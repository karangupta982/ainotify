from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        populate_by_name = True


class ProfilePayload(BaseModel):
    name: str
    title: str
    email_to: Optional[EmailStr] = None  # Optional: defaults to signup email if not provided
    background: str
    interests: str
    expertise_level: str
    preferences: dict


class ChannelsPayload(BaseModel):
    channel_ids: List[str]


class BillingCheckoutRequest(BaseModel):
    priceId: str


class PaymentVerificationRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str
