import json
import os
import pathlib
import time
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from google.oauth2 import service_account
from pydantic import BaseModel, Field

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def create_firestore_client() -> firestore.Client:
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if credentials_json:
        try:
            credentials_info = json.loads(credentials_json)
        except json.JSONDecodeError as error:
            raise RuntimeError("GOOGLE_CREDENTIALS_JSON must contain valid JSON") from error

        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        project_id = credentials_info.get("project_id")
        return firestore.Client(project=project_id, credentials=credentials)

    return firestore.Client()


USE_FIRESTORE = os.getenv("USE_FIRESTORE", "true").strip().lower() != "false"

if USE_FIRESTORE:
    try:
        db = create_firestore_client()
        dreams_collection = db.collection("dreams")
    except Exception:
        dreams_collection = None
else:
    dreams_collection = None

local_dreams = []


class DreamItem(BaseModel):
    location: str = Field(..., min_length=1)
    priority: str = Field(..., regex="^(High|Medium|Low)$")
    budget: int = Field(..., ge=0)


class DreamResponse(DreamItem):
    id: str
    createdAt: float


@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = pathlib.Path("static/index.html")
    return html_path.read_text(encoding="utf-8")


@app.get("/api/hello")
def read_api_hello():
    return {
        "message": "Hello from Trip Dreams API!",
        "firestore": dreams_collection is not None,
    }


@app.get("/api/dreams", response_model=List[DreamResponse])
def list_dreams():
    if dreams_collection is None:
        return [DreamResponse(**dream) for dream in local_dreams]

    docs = dreams_collection.order_by("createdAt", direction=firestore.Query.DESCENDING).stream()
    dreams = []
    for doc in docs:
        data = doc.to_dict()
        dreams.append(
            DreamResponse(
                id=doc.id,
                location=data.get("location", ""),
                priority=data.get("priority", "Medium"),
                budget=data.get("budget", 0),
                createdAt=data.get("createdAt", 0),
            )
        )
    return dreams


@app.post("/api/dreams", response_model=DreamResponse)
def create_dream(dream: DreamItem):
    payload = dream.dict()
    payload["createdAt"] = time.time()

    if dreams_collection is None:
        payload["id"] = f"local-{len(local_dreams) + 1}"
        local_dreams.insert(0, payload)
        return DreamResponse(**payload)

    new_doc = dreams_collection.document()
    new_doc.set(payload)
    return DreamResponse(id=new_doc.id, **payload)
