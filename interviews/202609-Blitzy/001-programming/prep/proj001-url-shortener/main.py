import random
import string
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI(title="URL Shortener API")

# ---------------------------------------------------------
# In-Memory Database Strategy
# key: short_code (str) -> value: dict record
# ---------------------------------------------------------
db: dict[str, dict] = {}


def generate_short_code(length: int = 6) -> str:
    """Helper to generate a random alphanumeric string."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


# ---------------------------------------------------------
# Pydantic Schemas (Request/Response Models)
# ---------------------------------------------------------
class ShortenRequest(BaseModel):
    url: HttpUrl
    custom_code: str | None = Field(None, min_length=3, max_length=10)
    ttl_seconds: int | None = Field(None, gt=0)


class ShortenResponse(BaseModel):
    short_code: str
    original_url: str
    created_at: datetime
    expires_at: datetime | None = None


class StatsResponse(BaseModel):
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime
    expires_at: datetime | None = None


# ---------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------


@app.get("/")
def read_root():
    """Root health check to prevent 404 on base URL."""
    return {"status": "ok", "message": "URL Shortener API running. Visit /docs for UI."}


@app.post(
    "/shorten", status_code=status.HTTP_201_CREATED, response_model=ShortenResponse
)
def create_short_url(payload: ShortenRequest):
    # 1. Determine or validate short_code
    if payload.custom_code:
        if payload.custom_code in db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Custom code '{payload.custom_code}' is already taken.",
            )
        code = payload.custom_code
    else:
        # Collision handling for random generation
        code = generate_short_code()
        while code in db:
            code = generate_short_code()

    now = datetime.now(timezone.utc)
    expires_at = None
    if payload.ttl_seconds:
        expires_at = datetime.fromtimestamp(
            now.timestamp() + payload.ttl_seconds, tz=timezone.utc
        )

    # 2. Store in-memory
    record = {
        "short_code": code,
        "original_url": str(payload.url),
        "clicks": 0,
        "created_at": now,
        "expires_at": expires_at,
    }
    db[code] = record

    return record


@app.get("/r/{short_code}", status_code=status.HTTP_200_OK)
def redirect_or_resolve(short_code: str):
    # 1. Existence Check
    if short_code not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
        )

    record = db[short_code]

    # 2. Expiration Check
    if record["expires_at"] and datetime.now(timezone.utc) > record["expires_at"]:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="Short URL has expired"
        )

    # 3. Update Clicks State
    record["clicks"] += 1

    return {"original_url": record["original_url"]}


@app.get(
    "/stats/{short_code}", status_code=status.HTTP_200_OK, response_model=StatsResponse
)
def get_stats(short_code: str):
    if short_code not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
        )
    return db[short_code]
