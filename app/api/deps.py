import os
from fastapi import Depends, HTTPException, Request, status
from app.api.security import decode_token, SESSION_COOKIE_NAME
from app.database.mongo import get_db


def get_mongo():
    return get_db()


def get_current_user(req: Request, db=Depends(get_mongo)):
    token = req.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db["users"].find_one({"_id": payload["sub"]})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


