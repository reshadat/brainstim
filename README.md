<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo.svg" width="420" alt="BrainStim">
  </picture>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-16161a?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/badge/python-3.10%2B-16161a?style=flat-square" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/backend-FastAPI-16161a?style=flat-square" alt="FastAPI">
  <img src="https://img.shields.io/badge/model-Meta%20TRIBEv2-e11d74?style=flat-square" alt="TRIBEv2">
  <img src="https://img.shields.io/badge/GPU-not%20required%20(simulation%20mode)-16161a?style=flat-square" alt="Simulation mode">
</p>

<p align="center"><b>See what a video, a song, or a poem does to a brain.</b></p>

Upload a video, audio clip, or piece of text and watch which parts of your brain it activates — predicted fMRI activity across 20,484 cortical vertices, mapped to 360 named regions and translated into psychological experiences.

Built on [Meta TRIBEv2](https://github.com/facebookresearch/tribev2), the state-of-the-art brain encoding model from Meta AI Research.

**Not a medical tool.** Exploration and creative use only.

---

## What it does

1. You upload media (video, audio, or text)
2. TRIBEv2 predicts fMRI brain activations across 20,484 cortical vertices
3. Vertices are mapped to the HCP-MMP1 atlas (360 named cortical regions)
4. Each region is translated to psychological experiences (e.g. V1 → visual edges, Broca's → language production)
5. Results stream back with animated brain visualizations, waveform, and stimulation tips

---

## Try it instantly (no model required)

BrainStim ships with a **simulation mode** so you can explore the full interface
without installing the multi-gigabyte TRIBEv2 stack:

```bash
git clone https://github.com/reshadat/brainstim
cd brainstim

# Install the deps (see note below — start.sh alone is not enough)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt fastapi "uvicorn[standard]" python-multipart soundfile

# Launch
python -m uvicorn main:app --app-dir api --port 8000
```

Open `http://localhost:8000` and pick one of the sample stimuli ("Ocean
Documentary", "Live Jazz Set", "Spoken Poem", "Thriller Trailer", "Stand-up
Comedy"). Each runs a complete analysis with **real nilearn cortical-surface
renders** driven by synthesized activation, plus region and emotion breakdowns
drawn from the same HCP-MMP1 atlas data the live pipeline uses.

If you upload your own media while TRIBEv2 isn't installed, BrainStim
automatically falls back to simulation so the experience still works
end-to-end. A badge marks any result that came from simulation.

> **Note:** `start.sh` only installs the web-server packages
> (`fastapi`, `uvicorn`, `python-multipart`, `soundfile`). It does **not**
> install `requirements.txt`, so simulation mode needs `nilearn`, `matplotlib`,
> and `numpy` installed separately — hence the explicit `pip install -r
> requirements.txt` above. The `fsaverage5` mesh (~10 MB) downloads once on
> first run.

---

## Setup (full TRIBEv2 pipeline)

The live pipeline runs real fMRI prediction with
[Meta's TRIBEv2](https://github.com/facebookresearch/tribev2). It needs a
capable machine (ideally a CUDA GPU) and several GB of model downloads. On a
laptop — especially Apple Silicon without CUDA — expect slow inference and
prefer simulation mode above.

### Prerequisites

- **Python 3.11+** (TRIBEv2 requires 3.11+; the simulation venv's 3.9 is *not*
  enough for the full pipeline)
- ffmpeg (for video/audio processing)
- [TRIBEv2](https://github.com/facebookresearch/tribev2) installed (see below)
- A Hugging Face account with **approved access to
  [`meta-llama/Llama-3.2-3B`](https://huggingface.co/meta-llama/Llama-3.2-3B)**.
  The model is gated: request access on its model page (approval is typically
  minutes to hours), create a read token, then `huggingface-cli login`.
  TRIBEv2 loads Llama 3.2 internally, so inference fails without this even after
  everything else installs.

> TRIBEv2 weights ([`facebook/tribev2`](https://huggingface.co/facebook/tribev2))
> are released under **CC BY-NC 4.0 — non-commercial use only**.

### 1. System dependencies (macOS / Homebrew)

```bash
brew install python@3.12 ffmpeg
```

### 2. Install TRIBEv2

```bash
git clone https://github.com/facebookresearch/tribev2
cd tribev2
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[plotting]"
```

This pulls PyTorch and the multimodal encoders — several GB. The first
inference also downloads the `facebook/tribev2` weights plus supporting models
(Llama 3.2, V-JEPA2, Wav2Vec-BERT); subsequent runs use the cache.

### 3. Authenticate with Hugging Face

```bash
huggingface-cli login   # paste a token from an account approved for Llama-3.2-3B
```

### 4. Run BrainStim against the live pipeline

```bash
git clone https://github.com/reshadat/brainstim
cd brainstim

# Point VENV at the tribev2 environment created in step 2:
VENV=/path/to/tribev2/.venv ./start.sh

# Or activate that venv first, then:
./start.sh

# Custom port:
./start.sh 9000
```

Open `http://localhost:8000`. API docs at `http://localhost:8000/docs`. With
TRIBEv2 importable and Llama access granted, uploads run real inference and
results no longer carry the `"simulated": true` badge.

> **Note:** `start.sh` falls back to system/active Python when `VENV` is unset.
> Either set `VENV` to your real tribev2 virtualenv (e.g.
> `/path/to/tribev2/.venv`) or activate that environment before running.

---

## API

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/infer` | Upload file → returns `job_id` |
| GET | `/api/samples` | List sample stimuli for simulation mode |
| POST | `/api/demo?scenario_id=…` | Run a simulated analysis on a sample → returns `job_id` |
| GET | `/api/job/{id}` | Poll job status and progress |
| GET | `/api/job/{id}/stream` | SSE stream of live progress |
| GET | `/api/job/{id}/results` | Full results: frames, ROIs, waveform |
| GET | `/api/brain_feelings` | Brain region → feelings mapping |

Simulated results carry `"simulated": true` and a `"scenario"` label in the
results payload.

Results payload:

```json
{
  "n_timesteps": 53,
  "n_vertices": 20484,
  "frames": ["<base64 PNG>", "..."],
  "waveform": "<base64 PNG>",
  "top_regions": [
    {
      "roi": "V1-lh",
      "activation": 0.84,
      "name": "Primary Visual Cortex",
      "experience": "Raw edges, brightness, contrast",
      "category": "Visual",
      "tip": "Add vivid imagery..."
    }
  ],
  "emotions": [
    { "emotion": "Curiosity", "percentage": 34.2 }
  ],
  "words": [{ "text": "hello", "start": 1.2, "duration": 0.3 }]
}
```

---

## Project structure

```
brainstim/
├── api/
│   ├── main.py        # FastAPI app and routes
│   ├── inference.py   # TRIBEv2 pipeline + job store
│   ├── rendering.py   # Brain frame (nilearn) + waveform (matplotlib)
│   ├── demo.py        # Simulation mode: synthetic activation + sample stimuli
│   └── data.py        # HCP-MMP1 region → feelings + stimulation tips
├── web/
│   └── index.html     # Single-file frontend (Tailwind + vanilla JS)
├── requirements.txt
└── start.sh
```

---

## Supported inputs

| Type | Extensions |
|------|-----------|
| Video | `.mp4` `.avi` `.mkv` `.mov` `.webm` |
| Audio | `.wav` `.mp3` `.flac` `.ogg` |
| Text | `.txt` |

---

## Known limitations

- No image support — TRIBEv2 processes temporal media only
- Jobs are lost on server restart (result JSON files survive; job index doesn't)
- Single-user, no auth — designed for local use
- Inference takes 1–5 minutes depending on file length and hardware

---

## License

MIT
