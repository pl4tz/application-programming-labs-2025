"""Module for audio visualization."""

import matplotlib.pyplot as plt
import numpy as np


def plot_audio(
    original: np.ndarray,
    reversed_audio: np.ndarray,
    samplerate: int
) -> None:
    """Plot original and reversed audio signals."""
    time_original = np.linspace(
        0, len(original) / samplerate, num=len(original)
    )
    time_reversed = np.linspace(
        0, len(reversed_audio) / samplerate, num=len(reversed_audio)
    )

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(time_original, original)
    plt.title("Original Audio")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")

    plt.subplot(2, 1, 2)
    plt.plot(time_reversed, reversed_audio)
    plt.title("Reversed Audio")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.show()