"""Main module for Lab 2 Variant 21."""

import argparse

from downloader import create_csv, download_files
from parser_module import collect_audio_links


def main() -> None:
    """Program entry point."""
    parser = argparse.ArgumentParser(description="Lab 2 Variant 21")
    parser.add_argument("--save_path", required=True)
    parser.add_argument("--csv_path", required=True)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--min_duration", type=int, default=10)

    args = parser.parse_args()

    if args.count < 50 or args.count > 1000:
        print("Количество должно быть от 50 до 1000")
        return

    links = collect_audio_links(args.min_duration, args.count)

    if not links:
        print("Подходящих файлов не найдено.")
        return

    if len(links) < args.count:
        print("Внимание: найдено меньше файлов, чем запрошено.")

    downloaded = download_files(links, args.save_path)
    create_csv(downloaded, args.csv_path)

    print("Готово.")


if __name__ == "__main__":
    main()