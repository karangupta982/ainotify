from fastapi import APIRouter, Depends
from app.api.deps import get_current_user, get_mongo
from app.api.schemas import ProfilePayload
from app.database.repository import Repository
from app.database.models import SubscriptionStatus

router = APIRouter(prefix="/api", tags=["profile"])


@router.get("/profile")
def get_profile(user=Depends(get_current_user), db=Depends(get_mongo)):
    doc = db["profiles"].find_one({"_id": user["_id"]})
    if not doc:
        return {"profile": None}
    doc["_id"] = str(doc["_id"])
    return {"profile": doc}


@router.post("/profile")
def upsert_profile(payload: ProfilePayload, user=Depends(get_current_user), db=Depends(get_mongo)):
    """Create/update profile and create subscription entry if it doesn't exist."""
    from fastapi import HTTPException
    from sqlalchemy.exc import ProgrammingError
    
    user_id = str(user["_id"])
    user_email = user.get("email")  # Signup email
    
    # Prepare profile data - if email_to not provided, use signup email
    profile_data = payload.model_dump()
    if not profile_data.get("email_to"):
        profile_data["email_to"] = user_email
    
    # Store in MongoDB
    db["profiles"].update_one(
        {"_id": user["_id"]},
        {"$set": {"profile": profile_data, "_id": user["_id"]}},
        upsert=True,
    )
    
    # Create subscription entry in PostgreSQL if it doesn't exist
    try:
        repo = Repository()
        existing_subscription = repo.get_user_subscription(user_id)
        if not existing_subscription:
            repo.create_user_subscription(
                user_id=user_id,
                status=SubscriptionStatus.TRIAL,
                plan=None,
                trial_days=2
            )
    except ProgrammingError as e:
        if "does not exist" in str(e):
            raise HTTPException(
                status_code=500,
                detail="Database tables not created. Please run: python -m app.database.create_tables"
            )
        raise
    
    return {"success": True}

