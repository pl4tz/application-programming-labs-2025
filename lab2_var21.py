import argparse
import csv
import os
import random
from typing import List

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


BASE_URL: str = "https://mixkit.co/free-sound-effects/discover/"

CATEGORIES: List[str] = [
    "nature",
    "animals",
    "transport",
    "technology",
    "people",
    "game",
    "urban",
]


def parse_duration(text: str) -> int:
    """Convert duration string (MM:SS) to seconds."""
    try:
        parts = text.strip().split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
    except ValueError:
        return 0
    return 0


def collect_audio_links(min_duration: int, needed_count: int) -> List[str]:
    """Collect audio links filtered by minimum duration."""
    headers = {"User-Agent": "Mozilla/5.0"}

    categories = CATEGORIES[:]
    random.shuffle(categories)

    collected: List[str] = []
    used_categories: List[str] = []

    for category in categories:
        if len(collected) >= needed_count:
            break

        url = BASE_URL + category + "/"
        print("\nТема:", category)
        print("Парсим:", url)

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except RequestException:
            print("Ошибка запроса, пропускаем.")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        audio_blocks = soup.find_all("div", {"data-test-id": "audio-player"})
        duration_blocks = soup.find_all("div", {"data-test-id": "duration"})

        before_count = len(collected)

        for block, duration_block in zip(audio_blocks, duration_blocks):
            seconds = parse_duration(duration_block.text)

            if seconds > min_duration:
                link = block.get("data-audio-player-preview-url-value")

                if link and link.endswith(".mp3") and link not in collected:
                    collected.append(link)

        added = len(collected) - before_count
        print(f"Добавлено из темы: {added}")
        print("Всего собрано:", len(collected))

        if added > 0:
            used_categories.append(category)

    print("\nИспользованные темы:", used_categories)
    print("ИТОГО найдено:", len(collected))

    return collected[:needed_count]


def download_files(links: List[str], save_path: str) -> List[str]:
    """Download audio files from provided links."""
    os.makedirs(save_path, exist_ok=True)
    downloaded: List[str] = []

    for i, link in enumerate(links):
        filename = os.path.join(save_path, f"audio_{i+1}.mp3")
        print(f"Скачиваем {i+1}/{len(links)}")

        try:
            r = requests.get(link, stream=True, timeout=10)
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            downloaded.append(filename)
        except (RequestException, OSError):
            print("Ошибка скачивания:", link)

    return downloaded


def create_csv(file_paths: List[str], csv_path: str) -> None:
    """Create CSV annotation file with absolute and relative paths."""
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["absolute_path", "relative_path"])

            for path in file_paths:
                writer.writerow([os.path.abspath(path), os.path.relpath(path)])

        print("CSV создан.")
    except OSError:
        print("Ошибка при создании CSV.")


class AudioIterator:
    """Iterator for audio files from CSV file or directory."""

    def __init__(self, source: str) -> None:
        if os.path.isfile(source):
            self.file = open(source, encoding="utf-8")
            self.reader = csv.reader(self.file)
            next(self.reader)
            self.mode = "csv"
        elif os.path.isdir(source):
            self.files = [
                os.path.join(source, f)
                for f in os.listdir(source)
                if f.endswith(".mp3")
            ]
            self.index = 0
            self.mode = "dir"
        else:
            raise ValueError("Неверный источник")

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self.mode == "csv":
            try:
                return next(self.reader)[0]
            except StopIteration:
                self.file.close()
                raise
        else:
            if self.index >= len(self.files):
                raise StopIteration
            file = self.files[self.index]
            self.index += 1
            return file


def main() -> None:
    """Program entry point."""
    parser = argparse.ArgumentParser()
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

    print("\nГотово.")


if __name__ == "__main__":
    main()
