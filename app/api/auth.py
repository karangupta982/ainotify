from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.api.schemas import SignupRequest, LoginRequest, UserOut
from app.api.security import (
    hash_password,
    verify_password,
    create_token,
    SESSION_COOKIE_NAME,
)
from app.api.deps import get_mongo

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=UserOut)
def signup(payload: SignupRequest, res: Response, db=Depends(get_mongo)):
    if db["users"].find_one({"email": payload.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_doc = {
        "_id": payload.email,  # simple key; could be ObjectId but email is unique
        "name": payload.name,
        "email": payload.email,
        "password": hash_password(payload.password),
        "created_at": datetime.utcnow(),
    }
    db["users"].insert_one(user_doc)

    token = create_token(sub=user_doc["_id"], email=user_doc["email"])
    # res.set_cookie(
    #     SESSION_COOKIE_NAME,
    #     token,
    #     httponly=True,
    #     secure=False,
    #     samesite="lax",
    #     max_age=7 * 24 * 3600,
    # )

    res.set_cookie(
        SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=True,          # REQUIRED for HTTPS
        samesite="none",      # REQUIRED for cross-site
        max_age=7 * 24 * 3600,
    )
    return user_doc


@router.post("/login", response_model=UserOut)
def login(payload: LoginRequest, res: Response, db=Depends(get_mongo)):
    user = db["users"].find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user.get("password", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_token(sub=user["_id"], email=user["email"])
    # res.set_cookie(
    #     SESSION_COOKIE_NAME,
    #     token,
    #     httponly=True,
    #     secure=False,
    #     samesite="lax",
    #     max_age=7 * 24 * 3600,
    # )

    res.set_cookie(
        SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=True,          # REQUIRED for HTTPS
        samesite="none",      # REQUIRED for cross-site
        max_age=7 * 24 * 3600,
    )
    return user


@router.post("/logout")
def logout(res: Response):
    res.delete_cookie(SESSION_COOKIE_NAME)
    return {"success": True}

