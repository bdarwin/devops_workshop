"""Front-end + backend API for the Travel Concierge."""

import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app import __version__, agents, llm, prompts

app = FastAPI(title="Go East Travel Concierge")


class Chat(BaseModel):
    message: str
    customer: str = "anon"


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {
        "app": __version__,
        "model": llm.MODEL,
        "prompt_version": prompts.VERSION,
        "env": os.environ.get("CONCIERGE_ENV", "local"),
        "live_llm": llm.live(),
    }


@app.post("/chat")
def chat(body: Chat):
    return agents.handle(body.message, body.customer)


@app.get("/")
def index():
    return FileResponse("static/index.html")
