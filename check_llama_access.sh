#!/usr/bin/env bash
# Checks if LLaMA 3.2-3B access has been granted on HuggingFace.
# If approved, runs a full inference test and sends result to stdout.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${VENV:-$SCRIPT_DIR/../tribev2/path/to/venv}"
PYTHON="$VENV/bin/python"
LOG="$SCRIPT_DIR/llama_check.log"

echo "$(date) — Checking LLaMA 3.2 access…" >> "$LOG"

ACCESS=$("$PYTHON" -c "
from huggingface_hub import model_info
try:
    info = model_info('meta-llama/Llama-3.2-3B')
    print('granted')
except Exception as e:
    if '403' in str(e) or 'gated' in str(e).lower():
        print('pending')
    else:
        print('error: ' + str(e))
" 2>/dev/null)

echo "$(date) — Status: $ACCESS" >> "$LOG"

if [ "$ACCESS" = "granted" ]; then
    echo "$(date) — ACCESS GRANTED! Running inference test…" >> "$LOG"

    "$PYTHON" -c "
from tribev2 import TribeModel
import numpy as np

model = TribeModel.from_pretrained('facebook/tribev2', cache_folder='$SCRIPT_DIR/cache')
df = model.get_events_dataframe(audio_path='/tmp/test_audio.mp3')
preds, segments = model.predict(events=df)
print(f'SUCCESS — preds: {preds.shape}, {len(segments)} segments')
print(f'Top activation: {preds.mean(axis=0).max():.4f}')
" >> "$LOG" 2>&1

    echo "$(date) — Test complete. Removing cron." >> "$LOG"
    # Remove this cron entry once approved
    crontab -l 2>/dev/null | grep -v 'check_llama_access' | crontab -
    echo "$(date) — Cron removed." >> "$LOG"
else
    echo "$(date) — Still waiting…" >> "$LOG"
fi
