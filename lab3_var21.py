import argparse
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import os


def reverse_audio(data):
    return data[::-1]


def plot_audio(original, reversed_audio, samplerate):
    time_original = np.linspace(0, len(original) / samplerate, num=len(original))
    time_reversed = np.linspace(0, len(reversed_audio) / samplerate, num=len(reversed_audio))

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_path", required=True)

    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        print("Файл не найден.")
        return

    data, samplerate = sf.read(args.input_path)

    print("Размер массива:", data.shape)
    print("Частота дискретизации:", samplerate)
    print("Длительность (сек):", len(data) / samplerate)

    reversed_data = reverse_audio(data)

    plot_audio(data, reversed_data, samplerate)

    sf.write(args.output_path, reversed_data, samplerate)

    print("Файл сохранён:", args.output_path)


if __name__ == "__main__":
    main()