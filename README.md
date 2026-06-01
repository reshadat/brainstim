# BrainStim

Upload a video, audio clip, or piece of text and see which parts of your brain it activates — predicted fMRI activity mapped to real psychological experiences.

Built on [META TRIBEv2](https://github.com/facebookresearch/thalamus), the state-of-the-art brain encoding model from Meta AI Research.

**Not a medical tool.** Exploration and creative use only.

---

## What it does

1. You upload media (video, audio, or text)
2. TRIBEv2 predicts fMRI brain activations across 20,484 cortical vertices
3. Vertices are mapped to the HCP-MMP1 atlas (360 named cortical regions)
4. Each region is translated to psychological experiences (e.g. V1 → visual edges, Broca's → language production)
5. Results stream back with animated brain visualizations, waveform, and stimulation tips

---

## Setup

### Prerequisites

- Python 3.10+
- [TRIBEv2](https://github.com/facebookresearch/thalamus) installed (see below)
- ffmpeg (for video/audio processing)

### Install TRIBEv2

```bash
git clone https://github.com/facebookresearch/thalamus
cd thalamus
pip install -e ".[plotting]"
```

First run downloads ~500 MB (tribev2-mini) plus supporting models (LLaMA 3.2, V-JEPA2, Wav2Vec-BERT) — several GB total. Subsequent runs use the cache.

### Run BrainStim

```bash
git clone https://github.com/reshadat/brainstim
cd brainstim

# If tribev2 is in a separate venv:
VENV=../thalamus/path/to/venv ./start.sh

# Or if tribev2 is in your system Python:
./start.sh

# Custom port:
./start.sh 9000
```

Open `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

---

## API

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/infer` | Upload file → returns `job_id` |
| GET | `/api/job/{id}` | Poll job status and progress |
| GET | `/api/job/{id}/stream` | SSE stream of live progress |
| GET | `/api/job/{id}/results` | Full results: frames, ROIs, waveform |
| GET | `/api/brain_feelings` | Brain region → feelings mapping |

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
│   ├── rendering.py   # Brain frame (PyVista) + waveform (matplotlib)
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
