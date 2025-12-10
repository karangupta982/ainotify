import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, profile, channels, billing
from app.api.deps import get_mongo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Notify API", version="1.0.0")

origins = [os.getenv("FRONTEND_URL", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    db = get_mongo()
    # simple connectivity check
    db.command("ping")
    logger.info("MongoDB connected successfully")


@app.get("/api/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(channels.router)
app.include_router(billing.router)

