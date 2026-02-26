"""Module for audio processing operations."""

from typing import Tuple

import numpy as np
import soundfile as sf


def read_audio(path: str) -> Tuple[np.ndarray, int]:
    """Read audio file and return data with samplerate."""
    data, samplerate = sf.read(path)
    return data, samplerate


def write_audio(path: str, data: np.ndarray, samplerate: int) -> None:
    """Write audio data to file."""
    sf.write(path, data, samplerate)


def reverse_audio(data: np.ndarray) -> np.ndarray:
    """Return reversed audio signal."""
    return data[::-1]