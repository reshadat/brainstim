"""
TRIBEv2 inference pipeline and in-memory job store.
"""
import os
import json
import threading
import traceback
from pathlib import Path
from typing import Dict, Any

import numpy as np

from data import BRAIN_FEELINGS, STIMULATION_TIPS, EMOTION_CIRCUITS
from rendering import render_brain_frame, render_waveform

# ── job store (in-memory, sufficient for local/single-server use) ─────────────

jobs: Dict[str, Dict[str, Any]] = {}

# ── ROI analysis ───────────────────────────────────────────────────────────────


def get_top_regions(preds: np.ndarray, k: int = 12) -> list:
    mean_pred = preds.mean(axis=0)
    try:
        from tribev2.utils import get_hcp_labels, get_hcp_roi_indices

        hcp = get_hcp_labels(mesh="fsaverage5", hemi="both")

        # Compute per-ROI mean activation (avoids buggy get_topk_rois)
        roi_activations = {}
        for name in hcp:
            if name == "?":
                continue
            indices = hcp[name]
            if len(indices) > 0:
                roi_activations[name] = float(mean_pred[indices].mean())

        sorted_rois = sorted(roi_activations.items(), key=lambda x: x[1], reverse=True)[:k]

        results = []
        for name, activation in sorted_rois:
            # Strip hemisphere suffixes and prefixes for feelings lookup
            clean = name.replace("-lh", "").replace("-rh", "")
            clean = clean.replace("L_", "").replace("R_", "").replace("_ROI", "")

            feeling = BRAIN_FEELINGS.get(clean, {
                "name": clean,
                "experience": "Complex multimodal processing",
                "category": "Other",
            })
            results.append({
                "roi": name,
                "activation": activation,
                "name": feeling["name"],
                "experience": feeling["experience"],
                "category": feeling["category"],
                "tip": STIMULATION_TIPS.get(feeling["category"], ""),
            })
        return results

    except Exception:
        # Fallback: just rank raw vertices
        top_idx = np.argsort(mean_pred)[-k:][::-1]
        return [
            {
                "roi": f"vertex_{i}",
                "activation": float(mean_pred[i]),
                "name": f"{'Left' if i < 10242 else 'Right'} cortex (vertex {i})",
                "experience": "Brain activation",
                "category": "Other",
                "tip": "",
            }
            for i in top_idx
        ]


def score_emotions(preds: np.ndarray) -> list:
    """Score each emotion based on weighted region activations."""
    mean_pred = preds.mean(axis=0)

    try:
        from tribev2.utils import get_hcp_labels
        hcp = get_hcp_labels(mesh="fsaverage5", hemi="both")
    except Exception:
        return []

    scores = {}
    for emotion, config in EMOTION_CIRCUITS.items():
        total = 0.0
        weight_sum = 0.0
        for region, weight in config["regions"].items():
            indices = hcp.get(region, [])
            if len(indices) > 0:
                total += float(mean_pred[indices].mean()) * weight
                weight_sum += weight
        scores[emotion] = total / weight_sum if weight_sum > 0 else 0.0

    # Normalize to percentages (shift to positive, then to 0-100)
    min_score = min(scores.values())
    shifted = {k: v - min_score for k, v in scores.items()}
    total = sum(shifted.values())
    if total == 0:
        total = 1.0

    results = []
    for emotion, raw in sorted(shifted.items(), key=lambda x: x[1], reverse=True):
        pct = (raw / total) * 100
        results.append({
            "emotion": emotion,
            "percentage": round(pct, 1),
            "description": EMOTION_CIRCUITS[emotion]["description"],
            "color": EMOTION_CIRCUITS[emotion]["color"],
        })
    return results


# ── inference runner (background thread) ──────────────────────────────────────

RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

CACHE_DIR = Path(__file__).parent.parent / "cache"


def _update(job: dict, status: str, pct: int, msg: str):
    job.update(status=status, progress=pct, message=msg)


def run_inference(job_id: str, file_path: str, file_type: str):
    job = jobs[job_id]
    try:
        _update(job, "loading_model", 5, "Loading TRIBEv2 model (first run downloads ~500 MB)…")
        from tribev2 import TribeModel
        model = TribeModel.from_pretrained(
            "facebook/tribev2", cache_folder=str(CACHE_DIR)
        )

        _update(job, "extracting", 25, "Extracting events from media…")
        df = model.get_events_dataframe(**{f"{file_type}_path": file_path})

        _update(job, "predicting", 50, "Running brain activity prediction…")
        preds, segments = model.predict(events=df)

        _update(job, "rendering", 75, "Rendering brain visualizations…")
        vmax = float(np.percentile(np.abs(preds), 98))
        n_frames = min(len(preds), 20)

        frames = []
        for i in range(n_frames):
            frames.append(render_brain_frame(preds[i], vmax=vmax))
            job["progress"] = 75 + int(20 * i / n_frames)

        # Waveform
        waveform_b64 = ""
        if "type" in df.columns:
            audio_rows = df[df["type"] == "Audio"]
            if not audio_rows.empty:
                ap = audio_rows.iloc[0].get("filepath", "")
                if ap and os.path.exists(str(ap)):
                    waveform_b64 = render_waveform(str(ap))

        # Word timestamps
        words = []
        if "type" in df.columns:
            for _, row in df[df["type"] == "Word"].head(80).iterrows():
                words.append({
                    "text": str(row.get("text", "")),
                    "start": float(row.get("start", 0)),
                    "duration": float(row.get("duration", 0.3)),
                })

        top_regions = get_top_regions(preds)
        emotions = score_emotions(preds)

        result = {
            "n_timesteps": int(preds.shape[0]),
            "n_vertices":  int(preds.shape[1]),
            "vmax":        vmax,
            "frames":      frames,
            "waveform":    waveform_b64,
            "top_regions": top_regions,
            "emotions":    emotions,
            "words":       words,
        }
        rpath = RESULTS_DIR / f"{job_id}.json"
        with open(rpath, "w") as f:
            json.dump(result, f)

        job["result_path"] = str(rpath)
        _update(job, "done", 100, "Analysis complete!")

    except Exception as e:
        job.update(
            status="error",
            error=str(e),
            _traceback=traceback.format_exc(),
            message=f"Error: {e}",
        )


def start_job(job_id: str, file_path: str, file_type: str):
    t = threading.Thread(
        target=run_inference, args=(job_id, file_path, file_type), daemon=True
    )
    t.start()
