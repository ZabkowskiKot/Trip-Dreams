import json
import os
import pathlib
import time
from typing import List

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from google.oauth2 import service_account
from pydantic import BaseModel, Field

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Session middleware
SECRET_KEY = os.getenv("SESSION_SECRET", os.getenv("SECRET_KEY", "dev-secret-change-me"))
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# OAuth configuration
oauth = OAuth()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

OAUTH_ENABLED = bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)


def create_firestore_client() -> firestore.Client:
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if credentials_json:
        try:
            credentials_info = json.loads(credentials_json)
        except json.JSONDecodeError as error:
            raise RuntimeError("GOOGLE_CREDENTIALS_JSON or GOOGLE_APPLICATION_CREDENTIALS_JSON must contain valid JSON") from error

        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        project_id = credentials_info.get("project_id") or os.getenv("FIRESTORE_PROJECT_ID")
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
    priority: str = Field(..., pattern="^(High|Medium|Low)$")
    budget: int = Field(..., ge=0)


class DreamResponse(DreamItem):
    id: str
    createdAt: float


@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = pathlib.Path("static/index.html")
    return html_path.read_text(encoding="utf-8")
@app.get("/login")
async def login(request: Request):
    if not OAUTH_ENABLED:
        return HTMLResponse(
            "<h1>Google OAuth is not configured</h1><p>Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your environment.</p>",
            status_code=500,
        )
    redirect_uri = f"{BASE_URL.rstrip('/')}/auth"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth")
async def auth(request: Request):
    if not OAUTH_ENABLED:
        return HTMLResponse(
            "<h1>Google OAuth is not configured</h1><p>Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your environment.</p>",
            status_code=500,
        )
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to authorize")

    user = None
    try:
        user = await oauth.google.parse_id_token(request, token)
    except Exception:
        # fallback to userinfo endpoint
        try:
            user = await oauth.google.userinfo(request)
        except Exception:
            user = None

    if user is None:
        raise HTTPException(status_code=400, detail="Failed to obtain user info")

    request.session["user"] = dict(user)
    return RedirectResponse(url="/")

@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")

@app.get("/api/me")
def api_me(request: Request):
    user = request.session.get("user")
    if not user:
        return {"logged_in": False}
    return {"logged_in": True, "user": user}


@app.get("/api/config")
def api_config():
    return {"oauth_enabled": OAUTH_ENABLED}


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
def create_dream(request: Request, dream: DreamItem):
    # Require login to save
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required to save dreams")

    payload = dream.dict()
    payload["createdAt"] = time.time()
    payload["createdBy"] = {"email": user.get("email"), "name": user.get("name")}

    if dreams_collection is None:
        payload["id"] = f"local-{len(local_dreams) + 1}"
        local_dreams.insert(0, payload)
        return DreamResponse(**payload)

    new_doc = dreams_collection.document()
    new_doc.set(payload)
    return DreamResponse(id=new_doc.id, **payload)
