from fastapi import APIRouter, Depends
from app.api.deps import get_current_user, get_mongo
from app.api.schemas import ChannelsPayload
from app.database.repository import Repository

router = APIRouter(prefix="/api", tags=["channels"])


@router.get("/channels")
def get_channels(user=Depends(get_current_user), db=Depends(get_mongo)):
    """Get channels from MongoDB (for API responses)."""
    doc = db["channels"].find_one({"_id": user["_id"]})
    channel_ids = doc.get("channel_ids", []) if doc else []
    return {"channel_ids": channel_ids}


@router.post("/channels")
def upsert_channels(payload: ChannelsPayload, user=Depends(get_current_user), db=Depends(get_mongo)):
    """Store channels in both MongoDB (for API) and PostgreSQL (for pipeline)."""
    from fastapi import HTTPException
    from sqlalchemy.exc import ProgrammingError
    
    user_id = str(user["_id"])
    
    # Store in MongoDB (for API responses)
    db["channels"].update_one(
        {"_id": user["_id"]},
        {"$set": {"channel_ids": payload.channel_ids, "_id": user["_id"]}},
        upsert=True,
    )
    
    # Store in PostgreSQL (for pipeline)
    try:
        repo = Repository()
        repo.upsert_user_channels(user_id, payload.channel_ids)
    except ProgrammingError as e:
        if "does not exist" in str(e):
            raise HTTPException(
                status_code=500,
                detail="Database tables not created. Please run: python -m app.database.create_tables"
            )
        raise
    
    return {"success": True}

