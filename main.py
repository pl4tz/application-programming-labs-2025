"""Main module for Lab 3 Variant 21."""

import argparse
import os

from audio_processing import read_audio, reverse_audio, write_audio
from visualization import plot_audio


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Lab 3 Variant 21")
    parser.add_argument("--input_path", required=True, type=str)
    parser.add_argument("--output_path", required=True, type=str)

    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        print("Файл не найден.")
        return

    try:
        data, samplerate = read_audio(args.input_path)
    except Exception:
        print("Ошибка чтения аудиофайла.")
        return

    print("Размер массива:", data.shape)
    print("Частота дискретизации:", samplerate)
    print("Длительность (сек):", len(data) / samplerate)

    reversed_data = reverse_audio(data)

    plot_audio(data, reversed_data, samplerate)

    try:
        write_audio(args.output_path, reversed_data, samplerate)
    except Exception:
        print("Ошибка записи файла.")
        return

    print("Файл сохранён:", args.output_path)


if __name__ == "__main__":
    main()