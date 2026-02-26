import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


def reverse_audio(data: np.ndarray) -> np.ndarray:
    """Return reversed audio signal."""
    return data[::-1]


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


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True, type=str)
    parser.add_argument("--output_path", required=True, type=str)

    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        print("Файл не найден.")
        return

    try:
        data, samplerate = sf.read(args.input_path)
    except Exception:
        print("Ошибка чтения аудиофайла.")
        return

    print("Размер массива:", data.shape)
    print("Частота дискретизации:", samplerate)
    print("Длительность (сек):", len(data) / samplerate)

    reversed_data = reverse_audio(data)

    plot_audio(data, reversed_data, samplerate)

    try:
        sf.write(args.output_path, reversed_data, samplerate)
    except Exception:
        print("Ошибка записи файла.")
        return

    print("Файл сохранён:", args.output_path)


if __name__ == "__main__":
    main()
