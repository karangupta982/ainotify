import os
import hmac
import hashlib
import razorpay
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from app.api.deps import get_current_user
from app.api.schemas import BillingCheckoutRequest, PaymentVerificationRequest
from app.database.repository import Repository
from app.database.models import SubscriptionStatus

router = APIRouter(prefix="/api/billing", tags=["billing"])


def _get_razorpay_client():
    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    if not key_id or not key_secret:
        raise HTTPException(status_code=500, detail="Razorpay keys not configured")
    return razorpay.Client(auth=(key_id, key_secret))


def _amount_for_plan(plan: str) -> int:
    mapping = {
        "starter": int(os.getenv("RAZORPAY_AMOUNT_STARTER", "0") or 0),
        "pro": int(os.getenv("RAZORPAY_AMOUNT_PRO", "0") or 0),
    }
    amount = mapping.get(plan, 0)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Unknown or unpriced plan")
    return amount


@router.post("/checkout")
def create_checkout_session(payload: BillingCheckoutRequest, user=Depends(get_current_user)):
    plan = payload.priceId
    amount = _amount_for_plan(plan)
    currency = os.getenv("RAZORPAY_CURRENCY", "INR")
    client = _get_razorpay_client()

    order = client.order.create(
        {
            "amount": amount,  # paise
            "currency": currency,
            "payment_capture": 1,
            "notes": {"user": user["_id"], "plan": plan},
        }
    )

    return {
        "order_id": order["id"],
        "amount": amount,
        "currency": currency,
        "key_id": os.getenv("RAZORPAY_KEY_ID"),
        "plan": plan,
    }


@router.post("/verify-payment")
def verify_payment(payload: PaymentVerificationRequest, user=Depends(get_current_user)):
    """
    Verify payment immediately after Razorpay payment success.
    This endpoint verifies the payment signature and updates the subscription.
    """
    razorpay_payment_id = payload.razorpay_payment_id
    razorpay_order_id = payload.razorpay_order_id
    razorpay_signature = payload.razorpay_signature
    
    if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
        raise HTTPException(status_code=400, detail="Missing payment verification data")
    
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    if not key_secret:
        raise HTTPException(status_code=500, detail="Razorpay secret not configured")
    
    # Verify payment signature
    message = f"{razorpay_order_id}|{razorpay_payment_id}"
    expected_signature = hmac.new(
        key_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(expected_signature, razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid payment signature")
    
    # Get order details from Razorpay
    client = _get_razorpay_client()
    try:
        order = client.order.fetch(razorpay_order_id)
        payment = client.payment.fetch(razorpay_payment_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch payment details: {str(e)}")
    
    # Verify payment status
    if payment.get("status") != "captured":
        raise HTTPException(status_code=400, detail="Payment not captured")
    
    # Get plan from order notes
    notes = order.get("notes", {})
    plan = notes.get("plan")
    order_user_id = notes.get("user")
    
    # Verify this payment belongs to the current user
    if order_user_id != user["_id"]:
        raise HTTPException(status_code=403, detail="Payment does not belong to current user")
    
    if not plan:
        raise HTTPException(status_code=400, detail="Plan not found in order notes")
    
    # Update subscription in database
    repo = Repository()
    user_id = str(user["_id"])
    
    # Ensure subscription exists
    subscription = repo.get_user_subscription(user_id)
    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    
    if not subscription:
        # Create subscription if it doesn't exist
        # First create with ACTIVE status
        new_subscription = repo.create_user_subscription(
            user_id=user_id,
            status=SubscriptionStatus.ACTIVE,
            plan=plan,
            trial_days=0  # Not a trial, already paid
        )
        # Then update expires_at (create_user_subscription sets it for TRIAL only)
        repo.update_subscription(
            user_id=user_id,
            expires_at=expires_at
        )
    else:
        # Update existing subscription
        success = repo.update_subscription(
            user_id=user_id,
            status=SubscriptionStatus.ACTIVE,
            plan=plan,
            expires_at=expires_at
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update subscription")
    
    return {
        "status": "success",
        "message": "Payment verified and subscription updated",
        "plan": plan,
        "expires_at": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    }


@router.get("/status")
def get_subscription_status(user=Depends(get_current_user)):
    """Get current subscription status for the logged-in user."""
    repo = Repository()
    user_id = str(user["_id"])
    
    subscription = repo.get_user_subscription(user_id)
    if not subscription:
        return {
            "status": "trial",
            "plan": None,
            "expires_at": None,
            "display_name": "Trial (2 days)"
        }
    
    # Check if subscription is expired
    now = datetime.now(timezone.utc).replace(tzinfo=None)  # naive UTC
    is_expired = (
        subscription.subscription_expires_at and 
        subscription.subscription_expires_at < now
    )
    
    if is_expired or subscription.subscription_status == SubscriptionStatus.EXPIRED:
        status_display = "Expired"
    elif subscription.subscription_status == SubscriptionStatus.ACTIVE:
        status_display = subscription.subscription_plan.capitalize() if subscription.subscription_plan else "Active"
    else:
        status_display = "Trial (2 days)"
    
    return {
        "status": subscription.subscription_status.value,
        "plan": subscription.subscription_plan,
        "expires_at": subscription.subscription_expires_at.isoformat() if subscription.subscription_expires_at else None,
        "display_name": status_display
    }


@router.post("/webhook")
async def razorpay_webhook(request: Request, x_razorpay_signature: str = Header(None)):
    """Handle Razorpay webhook events to update subscription status."""
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    if not key_secret:
        raise HTTPException(status_code=500, detail="Razorpay secret not configured")
    
    body = await request.body()
    body_str = body.decode('utf-8')
    
    # Verify webhook signature
    expected_signature = hmac.new(
        key_secret.encode('utf-8'),
        body_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(expected_signature, x_razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
    
    # Parse webhook payload
    import json
    payload = json.loads(body_str)
    event = payload.get("event")
    payment_data = payload.get("payload", {}).get("payment", {}).get("entity", {})
    order_data = payload.get("payload", {}).get("order", {}).get("entity", {})
    
    # Handle payment success
    if event == "payment.captured":
        order_id = order_data.get("id")
        notes = order_data.get("notes", {})
        user_id = notes.get("user")
        plan = notes.get("plan")
        
        if not user_id or not plan:
            raise HTTPException(status_code=400, detail="Missing user or plan in order notes")
        
        # Update subscription
        repo = Repository()
        # Set subscription to active for 30 days
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        repo.update_subscription(
            user_id=str(user_id),
            status=SubscriptionStatus.ACTIVE,
            plan=plan,
            expires_at=expires_at
        )
        
        return {"status": "success", "message": "Subscription updated"}
    
    return {"status": "received"}
