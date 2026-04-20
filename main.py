import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from app.routes import router
from db import init_db, log_request_metric

load_dotenv()

app = FastAPI(title="URL Shortener", version="1.0.0")
app.include_router(router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.middleware("http")
async def access_log_middleware(request: Request, call_next):
    import time
    from datetime import datetime, timezone

    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - started) * 1000

    ts = datetime.now(timezone.utc).isoformat()
    line = (
        f"{ts} method={request.method} path={request.url.path} "
        f"status={response.status_code} response_time_ms={elapsed_ms:.2f}"
    )

    with open("access.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

    log_request_metric(request.method, request.url.path, response.status_code)
    return response


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
