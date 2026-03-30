import base64
import json
import logging
import os
import re
from datetime import datetime
from typing import Any, List, Optional

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {
    "application/pdf",
    # "image/jpeg",
    # "image/jpg",
    # "image/png",
    # "text/csv",
    # "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # xlsx
    # "application/vnd.ms-excel",  # xls
    "application/msword",  # doc
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # docx
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gmail Attachment Webhook")


# ─────────────────────────────────────────────
#  MODELS
# ─────────────────────────────────────────────


class AttachmentFile(BaseModel):
    fileName: str
    mimeType: str
    data: str  # base64 encoded string


class GmailPayload(BaseModel):
    subject: Optional[str] = None
    sender: Optional[str] = None
    email_id: Optional[str] = None
    files: Optional[Any] = []

    @field_validator("files", mode="before")
    @classmethod
    def parse_files(cls, v):
        """
        Normalize `files` to always be a list of dicts regardless of
        how n8n serializes it.
        """
        if v is None:
            return []
        # n8n sometimes JSON-stringifies the array
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except json.JSONDecodeError:
                return []
        # single attachment — wrap in list
        if isinstance(v, dict):
            return [v]
        if isinstance(v, list):
            return v
        return []


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────


def safe_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip()


def decode_base64(data: str) -> bytes:
    if data.startswith("data:") and "," in data:
        data = data.split(",", 1)[1]

    data = data.strip().replace("-", "+").replace("_", "/")
    missing = len(data) % 4
    if missing:
        data += "=" * (4 - missing)

    return base64.b64decode(data)


def save_file(email_id: str, filename: str, file_bytes: bytes) -> str:

    folder = os.path.join(UPLOAD_DIR, safe_filename(email_id or "unknown"))

    os.makedirs(folder, exist_ok=True)

    safe_name = safe_filename(filename)
    save_path = os.path.join(folder, safe_name)

    # Avoid overwriting — append microsecond timestamp
    if os.path.exists(save_path):
        return save_path

    with open(save_path, "wb") as f:
        f.write(file_bytes)

    return save_path


# ─────────────────────────────────────────────
#  MAIN WEBHOOK
# ─────────────────────────────────────────────


@app.post("/webhook/gmail-attachment")
async def receive_gmail_attachments(
    request: Request, background_tasks: BackgroundTasks
):
    try:
        raw_body = await request.json()
    except Exception:
        raw = await request.body()
        logger.error("Bad JSON body: %s", raw[:300])
        raise HTTPException(status_code=400, detail="Request body must be valid JSON")

    logger.info("Received payload — keys: %s", list(raw_body.keys()))

    try:
        payload = GmailPayload(**raw_body)
    except Exception as e:
        logger.error("Validation error: %s", e)
        raise HTTPException(status_code=422, detail=str(e))

    logger.info(
        "from=%s | subject=%s | files=%d",
        payload.sender,
        payload.subject,
        len(payload.files),
    )

    if not payload.files:
        return JSONResponse(
            {
                "email_id": payload.email_id,
                "sender": payload.sender,
                "subject": payload.subject,
                "message": "No attachments found",
                "total": 0,
            }
        )

    results = []

    for entry in payload.files:
        try:
            att = AttachmentFile(**(entry if isinstance(entry, dict) else entry.dict()))
        except Exception as e:
            results.append(
                {"filename": str(entry), "status": "error", "reason": str(e)}
            )
            continue

        if att.mimeType not in ALLOWED_TYPES:
            logger.warning(
                "Skipping %s — MIME %s not allowed", att.fileName, att.mimeType
            )
            results.append(
                {
                    "filename": att.fileName,
                    "status": "skipped",
                    "reason": f"MIME type not allowed: {att.mimeType}",
                }
            )
            continue

        try:
            file_bytes = decode_base64(att.data)
        except Exception as e:
            logger.error("Base64 error for %s: %s", att.fileName, e)
            results.append(
                {
                    "filename": att.fileName,
                    "status": "error",
                    "reason": f"Base64 error: {e}",
                }
            )
            continue

        try:
            path = save_file(payload.email_id, att.fileName, file_bytes)
            logger.info("Saved %s → %s (%d bytes)", att.fileName, path, len(file_bytes))
        except Exception as e:
            logger.error("Save error for %s: %s", att.fileName, e)
            results.append(
                {
                    "filename": att.fileName,
                    "status": "error",
                    "reason": f"Save error: {e}",
                }
            )
            continue

        proc = process_attachment(path, att.fileName, att.mimeType, background_tasks)

        results.append(
            {
                "filename": att.fileName,
                "content_type": att.mimeType,
                "saved_to": path,
                "size_bytes": len(file_bytes),
                "status": "success",
                "result": proc,
            }
        )

    return JSONResponse(
        {
            "email_id": payload.email_id,
            "sender": payload.sender,
            "subject": payload.subject,
            "total": len(payload.files),
            "processed": sum(1 for r in results if r["status"] == "success"),
            "skipped": sum(1 for r in results if r["status"] == "skipped"),
            "errors": sum(1 for r in results if r["status"] == "error"),
            "files": results,
        }
    )


def process_attachment(
    path: str, filename: str, content_type: str, background_tasks: BackgroundTasks
) -> dict:

    return {
        "message": f"Processed {filename}",
        "size_bytes": os.path.getsize(path),
    }


@app.get("/health")
def health():
    return {"status": "ok", "upload_dir": os.path.abspath(UPLOAD_DIR)}
