"""
Brain frame and waveform rendering — nilearn + matplotlib Agg (fully headless).

PyVista/VTK crashes on macOS when used from a non-main thread (NSWindow
limitation), so we use nilearn for all server-side brain rendering.
"""
import io
import os
import base64
import tempfile

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Cache fsaverage5 mesh (downloaded once by nilearn)
_fsa5 = None


def _get_fsa5():
    global _fsa5
    if _fsa5 is None:
        from nilearn import datasets
        _fsa5 = datasets.fetch_surf_fsaverage(mesh="fsaverage5")
    return _fsa5


def render_brain_frame(activation_row: np.ndarray, vmax: float = None) -> str:
    """
    Render a lateral-left view of one brain activation timestep.
    Returns a base64-encoded PNG string.
    """
    from nilearn import plotting

    fsa5 = _get_fsa5()

    if vmax is None or vmax == 0:
        vmax = max(float(np.percentile(np.abs(activation_row), 98)), 1e-6)

    left_data = activation_row[:10242]

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        tmppath = f.name

    try:
        plotting.plot_surf_stat_map(
            fsa5.infl_left,
            stat_map=left_data,
            bg_map=fsa5.sulc_left,
            hemi="left",
            view="lateral",
            colorbar=False,
            cmap="hot",
            vmax=vmax,
            bg_on_data=True,
            output_file=tmppath,
        )

        # Read rendered image, composite onto dark background
        img = plt.imread(tmppath)
        fig, ax = plt.subplots(1, 1, figsize=(3, 2.4))
        fig.patch.set_facecolor("#0a0a1a")
        ax.set_facecolor("#0a0a1a")
        ax.imshow(img)
        ax.axis("off")

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=80, bbox_inches="tight",
                    facecolor="#0a0a1a", pad_inches=0.02)
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")
    finally:
        if os.path.exists(tmppath):
            os.unlink(tmppath)


def render_waveform(audio_path: str) -> str:
    """
    Render audio waveform as a wide, dark image.
    Returns a base64-encoded PNG string.
    """
    try:
        import soundfile as sf
        data, _ = sf.read(audio_path)
        if len(data.shape) > 1:
            data = data.mean(axis=1)
        step = max(1, len(data) // 2000)
        data = data[::step]
    except Exception:
        data = np.random.randn(1000) * 0.3

    return _render_waveform_signal(np.asarray(data, dtype=float))


def render_synthetic_waveform(seed: int = 0, n: int = 1600) -> str:
    """
    Render a plausible speech/music-like waveform for simulation mode —
    no audio file required. Returns a base64-encoded PNG string.
    """
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 1, n)
    # Layered carriers + a slow amplitude envelope + bursty syllable gating.
    carrier = (
        np.sin(2 * np.pi * 9 * x) * 0.6
        + np.sin(2 * np.pi * 23 * x + 0.7) * 0.3
        + np.sin(2 * np.pi * 51 * x + 1.3) * 0.15
    )
    envelope = 0.35 + 0.65 * np.abs(np.sin(2 * np.pi * 2.3 * x + rng.uniform(0, 3)))
    syllables = (np.sin(2 * np.pi * 6 * x + rng.uniform(0, 3)) > -0.3).astype(float)
    noise = rng.standard_normal(n) * 0.05
    data = (carrier * envelope * syllables + noise) * 0.9
    return _render_waveform_signal(data)


def _render_waveform_signal(data: np.ndarray) -> str:
    """Shared waveform drawing for real and synthetic signals."""
    fig, ax = plt.subplots(figsize=(16, 1.2))
    fig.patch.set_facecolor("#0a0a1a")
    ax.set_facecolor("#0a0a1a")
    x = np.arange(len(data))
    ax.plot(x, data, color="#ff6b35", linewidth=0.6, alpha=0.9)
    ax.fill_between(x, data, alpha=0.25, color="#ff6b35")
    ax.axhline(0, color="#ff6b3540", linewidth=0.3)
    ax.set_xlim(0, len(data))
    ax.axis("off")
    plt.tight_layout(pad=0)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=80, bbox_inches="tight", facecolor="#0a0a1a")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")
