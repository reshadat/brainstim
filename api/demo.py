"""
Simulation mode — generate a complete, realistic-looking BrainStim result
without the heavy TRIBEv2 model.

Brain frames are rendered through the *real* nilearn surface renderer
(rendering.render_brain_frame), so the visualizations are genuine cortical
surface plots — only the underlying activation is synthesized. Regions and
emotions are drawn from the same curated atlas data the real pipeline uses,
so the UI looks and behaves identically to a live analysis.
"""
from __future__ import annotations

from typing import Callable, Optional

import numpy as np

from data import BRAIN_FEELINGS, EMOTION_CIRCUITS, STIMULATION_TIPS
from rendering import render_brain_frame, render_synthetic_waveform

N_FRAMES = 14
N_VERTICES = 20484

ProgressCb = Optional[Callable[[int, str], None]]


# ── sample stimuli ────────────────────────────────────────────────────────────
# Each scenario lists the cortical regions it should light up (most → least
# salient) and an emotional lean. Region keys are validated against
# BRAIN_FEELINGS; emotion keys against EMOTION_CIRCUITS.

SAMPLE_STIMULI = [
    {
        "id": "ocean",
        "title": "Ocean Documentary",
        "subtitle": "Nature film · narrated",
        "icon": "🌊",
        "accent": "#38bdf8",
        "media_type": "video",
        "has_audio": True,
        "regions": ["V1", "V4", "MT", "MST", "V6", "A1", "STGa", "7m", "PCC", "TPOJ1", "V2", "RSC"],
        "emotions": {"Awe": 1.0, "Calm": 0.85, "Curiosity": 0.7, "Engagement": 0.55, "Joy": 0.35, "Nostalgia": 0.25},
        "narration": "Beneath the surface a world of light and motion drifts in endless blue silence",
    },
    {
        "id": "jazz",
        "title": "Live Jazz Set",
        "subtitle": "Audio · improvised trio",
        "icon": "🎷",
        "accent": "#f59e0b",
        "media_type": "audio",
        "has_audio": True,
        "regions": ["A1", "A4", "A5", "STGa", "LBelt", "PBelt", "RI", "MBelt", "FEF", "OFC", "TA2", "55b"],
        "emotions": {"Joy": 1.0, "Engagement": 0.9, "Awe": 0.45, "Curiosity": 0.4, "Calm": 0.3, "Nostalgia": 0.3},
        "narration": None,
    },
    {
        "id": "poem",
        "title": "Spoken Poem",
        "subtitle": "Text · read aloud",
        "icon": "📜",
        "accent": "#a78bfa",
        "media_type": "text",
        "has_audio": True,
        "regions": ["TGd", "TGv", "STSdp", "STSva", "STSda", "PSL", "H", "EC", "PHA1", "PFm", "45", "A1"],
        "emotions": {"Nostalgia": 1.0, "Empathy": 0.8, "Calm": 0.6, "Curiosity": 0.45, "Awe": 0.4, "Joy": 0.3},
        "narration": "I remember the warmth of a summer that has long since gone but lingers still in me",
    },
    {
        "id": "thriller",
        "title": "Thriller Trailer",
        "subtitle": "Video · high tension",
        "icon": "🎬",
        "accent": "#f87171",
        "media_type": "video",
        "has_audio": True,
        "regions": ["MT", "V1", "FFC", "OFA", "p24", "Ig", "MI", "AVI", "FEF", "A1", "24dv", "MST"],
        "emotions": {"Tension": 1.0, "Engagement": 0.75, "Curiosity": 0.6, "Awe": 0.35, "Disgust": 0.25, "Joy": 0.15},
        "narration": None,
    },
    {
        "id": "comedy",
        "title": "Stand-up Comedy",
        "subtitle": "Video · live audience",
        "icon": "🎤",
        "accent": "#34d399",
        "media_type": "video",
        "has_audio": True,
        "regions": ["FFC", "OFA", "STGa", "45", "44", "OFC", "10r", "TPOJ1", "A1", "TE1a", "STSva", "PSL"],
        "emotions": {"Joy": 1.0, "Engagement": 0.8, "Empathy": 0.6, "Curiosity": 0.45, "Awe": 0.2, "Calm": 0.2},
        "narration": None,
    },
]

_BY_ID = {s["id"]: s for s in SAMPLE_STIMULI}


def list_stimuli() -> list:
    """Public metadata for the sample gallery (no internal weighting)."""
    return [
        {
            "id": s["id"],
            "title": s["title"],
            "subtitle": s["subtitle"],
            "icon": s["icon"],
            "accent": s["accent"],
            "media_type": s["media_type"],
        }
        for s in SAMPLE_STIMULI
    ]


def get_scenario(scenario_id: str) -> Optional[dict]:
    return _BY_ID.get(scenario_id)


def fallback_scenario(file_type: str, filename: str) -> dict:
    """
    Generic scenario used when a *real* upload arrives but TRIBEv2 isn't
    installed — keeps the experience working in simulation mode.
    """
    by_type = {
        "video": "ocean",
        "audio": "jazz",
        "text": "poem",
    }
    base = dict(_BY_ID[by_type.get(file_type, "ocean")])
    base = {**base, "id": f"upload-{file_type}", "title": filename, "subtitle": f"{file_type} · simulation"}
    return base


# ── synthesis ──────────────────────────────────────────────────────────────────


def _synthesize_preds(seed: int, n_t: int = N_FRAMES, n_hot: int = 7) -> np.ndarray:
    """
    Build a (n_t, 20484) activation tensor with a handful of smooth, pulsing
    hotspots over the left hemisphere (the rendered view). Indices that are
    close together land near each other on the cortical surface, so contiguous
    Gaussian bumps read as coherent active patches once plotted.
    """
    rng = np.random.default_rng(seed)
    preds = (rng.standard_normal((n_t, N_VERTICES)) * 0.05).astype(np.float32)

    centers = rng.integers(300, 9900, size=n_hot)
    widths = rng.integers(90, 280, size=n_hot)
    phases = rng.uniform(0, 2 * np.pi, size=n_hot)
    speeds = rng.uniform(0.35, 0.95, size=n_hot)

    for t in range(n_t):
        for c, w, ph, sp in zip(centers, widths, phases, speeds):
            amp = 0.5 + 1.1 * (0.5 + 0.5 * np.sin(ph + sp * t))
            lo, hi = max(0, c - w), min(N_VERTICES, c + w)
            idx = np.arange(lo, hi)
            preds[t, lo:hi] += amp * np.exp(-((idx - c) ** 2) / (2 * (w / 2.5) ** 2))
    return preds


def _build_top_regions(scenario: dict, k: int = 12) -> list:
    keys = scenario["regions"][:k]
    rng = np.random.default_rng(abs(hash(scenario["id"])) % (2 ** 32))
    out = []
    for i, key in enumerate(keys):
        act = max(0.05, 0.9 * (1 - 0.05 * i) + float(rng.uniform(-0.02, 0.02)))
        f = BRAIN_FEELINGS.get(
            key, {"name": key, "experience": "Complex multimodal processing", "category": "Other"}
        )
        out.append({
            "roi": f"{key}-{'lh' if i % 2 == 0 else 'rh'}",
            "activation": round(act, 4),
            "name": f["name"],
            "experience": f["experience"],
            "category": f["category"],
            "tip": STIMULATION_TIPS.get(f["category"], ""),
        })
    return out


def _build_emotions(scenario: dict) -> list:
    weights = scenario["emotions"]
    total = sum(weights.values()) or 1.0
    out = []
    for emotion, w in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        cfg = EMOTION_CIRCUITS.get(emotion, {})
        out.append({
            "emotion": emotion,
            "percentage": round(w / total * 100, 1),
            "description": cfg.get("description", ""),
            "color": cfg.get("color", "#94a3b8"),
        })
    return out


def _build_words(scenario: dict, n_t: int) -> list:
    text = scenario.get("narration")
    if not text:
        return []
    toks = text.split()
    return [
        {"text": tok, "start": round(i / max(1, len(toks)) * n_t, 2), "duration": 0.32}
        for i, tok in enumerate(toks)
    ]


def generate_demo_result(scenario: dict, progress_cb: ProgressCb = None) -> dict:
    """Produce a full result payload (same schema as the real pipeline)."""
    def report(pct: int, msg: str):
        if progress_cb:
            progress_cb(pct, msg)

    seed = abs(hash(scenario["id"])) % (2 ** 32)

    report(15, "Synthesizing neural activity (simulation)…")
    preds = _synthesize_preds(seed)

    report(45, "Mapping cortical activation patterns…")
    vmax = float(np.percentile(np.abs(preds), 98)) or 1.0

    report(60, "Rendering brain visualizations…")
    frames = []
    for i in range(len(preds)):
        frames.append(render_brain_frame(preds[i], vmax=vmax))
        report(60 + int(30 * (i + 1) / len(preds)), "Rendering brain visualizations…")

    report(92, "Decoding regions and emotions…")
    waveform = render_synthetic_waveform(seed) if scenario.get("has_audio") else ""

    return {
        "n_timesteps": int(preds.shape[0]),
        "n_vertices": int(preds.shape[1]),
        "vmax": vmax,
        "simulated": True,
        "scenario": scenario.get("title", "Simulation"),
        "frames": frames,
        "waveform": waveform,
        "top_regions": _build_top_regions(scenario),
        "emotions": _build_emotions(scenario),
        "words": _build_words(scenario, len(preds)),
    }
