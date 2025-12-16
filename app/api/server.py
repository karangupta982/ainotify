import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, profile, channels, billing
from app.api.deps import get_mongo

# Load environment variables early so MONGODB_URL and others are available.
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    db = get_mongo()
    # simple connectivity check
    db.command("ping")
    logger.info("MongoDB connected successfully")
    yield
    # Shutdown (if needed in future)
    logger.info("Shutting down...")


app = FastAPI(title="AI Notify API", version="1.0.0", lifespan=lifespan)

# origins = ["*"]
# origins = [os.getenv("FRONTEND_URL", "http://localhost:3000")]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ainotify.vercel.app",  
    ],
    allow_credentials=True,            # ✅ required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(channels.router)
app.include_router(billing.router)

