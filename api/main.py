"""
BrainStim API — FastAPI entry point.
Run with: uvicorn main:app --app-dir api --reload --port 8000
"""
import asyncio
import json
import os
import uuid
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

import demo
from data import BRAIN_FEELINGS
from inference import jobs, start_demo_job, start_job

# ── app ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="BrainStim API",
    description=(
        "Brain activation analysis from video / audio / text via META TRIBEv2.\n\n"
        "**Supported inputs:** video (.mp4 .avi .mkv .mov .webm), "
        "audio (.wav .mp3 .flac .ogg), text (.txt)"
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ── file type map ─────────────────────────────────────────────────────────────

_EXT_TO_TYPE: Dict[str, str] = {
    **dict.fromkeys([".mp4", ".avi", ".mkv", ".mov", ".webm"], "video"),
    **dict.fromkeys([".wav", ".mp3", ".flac", ".ogg"],         "audio"),
    **dict.fromkeys([".txt"],                                   "text"),
}

# ── helpers ───────────────────────────────────────────────────────────────────


def _public_job(job_id: str) -> dict:
    """Strip internal fields before returning to client."""
    return {k: v for k, v in jobs[job_id].items()
            if k not in ("result_path", "_traceback")}


# ── routes ────────────────────────────────────────────────────────────────────


@app.post("/api/infer", summary="Upload media and start brain analysis")
async def infer(file: UploadFile = File(...)):
    """
    Upload a **video**, **audio**, or **text** file and start a brain
    activation analysis job.

    Returns `job_id` — use it to poll or stream progress, then fetch results.
    """
    suffix = Path(file.filename).suffix.lower()
    file_type = _EXT_TO_TYPE.get(suffix)
    if not file_type:
        raise HTTPException(
            400,
            f"Unsupported file type '{suffix}'. "
            "Accepted: video (.mp4/.avi/.mkv/.mov/.webm), "
            "audio (.wav/.mp3/.flac/.ogg), text (.txt)",
        )

    job_id = str(uuid.uuid4())
    dest = UPLOAD_DIR / f"{job_id}{suffix}"
    with open(dest, "wb") as f:
        f.write(await file.read())

    jobs[job_id] = {
        "id": job_id,
        "status": "queued",
        "progress": 0,
        "message": "Queued…",
        "filename": file.filename,
        "file_type": file_type,
    }
    start_job(job_id, str(dest), file_type)
    return JSONResponse({"job_id": job_id})


@app.get("/api/samples", summary="List sample stimuli for simulation mode")
async def list_samples():
    """
    Sample stimuli that can be analyzed in simulation mode (no TRIBEv2
    required) — used to populate the demo gallery.
    """
    return JSONResponse(demo.list_stimuli())


@app.post("/api/demo", summary="Run a simulated analysis on a sample stimulus")
async def run_demo(scenario_id: str):
    """
    Start a fully simulated analysis for one of the sample stimuli. Produces
    realistic brain visualizations and region/emotion breakdowns without the
    TRIBEv2 model. Returns `job_id` — poll/stream it exactly like a real job.
    """
    scenario = demo.get_scenario(scenario_id)
    if scenario is None:
        raise HTTPException(404, f"Unknown sample '{scenario_id}'")

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "id": job_id,
        "status": "queued",
        "progress": 0,
        "message": "Queued…",
        "filename": scenario["title"],
        "file_type": scenario["media_type"],
        "simulated": True,
    }
    start_demo_job(job_id, scenario)
    return JSONResponse({"job_id": job_id})


@app.get("/api/job/{job_id}", summary="Get job status")
async def get_job(job_id: str):
    """Poll the status and progress of an inference job."""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    return JSONResponse(_public_job(job_id))


@app.get("/api/job/{job_id}/stream", summary="Stream job progress (SSE)")
async def stream_job(job_id: str):
    """
    Server-Sent Events stream — fires an event every second with job status.
    Closes automatically when status is `done` or `error`.
    """
    async def gen():
        while True:
            if job_id not in jobs:
                yield f"data: {json.dumps({'error': 'not found'})}\n\n"
                return
            payload = _public_job(job_id)
            yield f"data: {json.dumps(payload)}\n\n"
            if payload["status"] in ("done", "error"):
                return
            await asyncio.sleep(1)

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/job/{job_id}/results", summary="Fetch full inference results")
async def get_results(job_id: str):
    """
    Returns brain frame images (base64 PNG), waveform image, top activated
    ROIs with feelings mapping, and word-level timestamps.
    """
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    job = jobs[job_id]
    if job["status"] != "done":
        raise HTTPException(400, f"Job not complete (status: {job['status']})")
    rp = job.get("result_path")
    if not rp or not os.path.exists(rp):
        raise HTTPException(500, "Result file missing — job may have been lost on restart")
    with open(rp) as f:
        return JSONResponse(json.load(f))


@app.get("/api/brain_feelings", summary="Brain region → feelings mapping")
async def brain_feelings():
    """Full HCP-MMP1 region → psychological experience mapping."""
    return JSONResponse(BRAIN_FEELINGS)


# ── static frontend (must be mounted last) ────────────────────────────────────

_WEB_DIR = Path(__file__).parent.parent / "web"
app.mount("/", StaticFiles(directory=str(_WEB_DIR), html=True), name="static")
