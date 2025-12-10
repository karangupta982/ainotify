from fastapi import APIRouter, Depends
from app.api.deps import get_current_user, get_mongo
from app.api.schemas import ProfilePayload

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
    db["profiles"].update_one(
        {"_id": user["_id"]},
        {"$set": {"profile": payload.model_dump(), "_id": user["_id"]}},
        upsert=True,
    )
    return {"success": True}

