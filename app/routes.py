import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from app.services import make_code, validate_url
from db import (
    create_link,
    get_link,
    increment_click,
    requests_per_minute_last_hour,
    top_links,
    total_clicks,
    total_links,
)

router = APIRouter()


class ShortenRequest(BaseModel):
    url: str = Field(..., examples=["https://example.com"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/shorten")
def shorten(payload: ShortenRequest):
    if not validate_url(payload.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    code = make_code(payload.url)
    existing = get_link(code)
    if not existing:
        create_link(code, payload.url)

    port = int(os.getenv("PORT", "8000"))
    return {
        "short_code": code,
        "short_url": f"http://localhost:{port}/{code}",
    }


@router.get("/stats/{code}")
def stats(code: str):
    row = get_link(code)
    if not row:
        raise HTTPException(status_code=404, detail="Code not found")
    return {
        "code": row["code"],
        "url": row["url"],
        "clicks": row["clicks"],
        "created_at": row["created_at"],
    }


@router.get("/stats/dashboard")
def stats_dashboard():
    return {
        "total_links": total_links(),
        "total_clicks": total_clicks(),
        "top_5_links": top_links(5),
        "requests_per_minute_last_hour": requests_per_minute_last_hour(),
    }


@router.get("/{code}")
def redirect(code: str):
    row = get_link(code)
    if not row:
        raise HTTPException(status_code=404, detail="Code not found")
    increment_click(code)
    return RedirectResponse(row["url"], status_code=302)
