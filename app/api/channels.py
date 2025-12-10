from fastapi import APIRouter, Depends
from app.api.deps import get_current_user, get_mongo
from app.api.schemas import ChannelsPayload

router = APIRouter(prefix="/api", tags=["channels"])


@router.get("/channels")
def get_channels(user=Depends(get_current_user), db=Depends(get_mongo)):
    doc = db["channels"].find_one({"_id": user["_id"]})
    channel_ids = doc.get("channel_ids", []) if doc else []
    return {"channel_ids": channel_ids}


@router.post("/channels")
def upsert_channels(payload: ChannelsPayload, user=Depends(get_current_user), db=Depends(get_mongo)):
    db["channels"].update_one(
        {"_id": user["_id"]},
        {"$set": {"channel_ids": payload.channel_ids, "_id": user["_id"]}},
        upsert=True,
    )
    return {"success": True}

