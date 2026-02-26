"""Module for downloading audio files and creating CSV annotations."""

import csv
import os
from typing import List

import requests
from requests.exceptions import RequestException


def download_files(links: List[str], save_path: str) -> List[str]:
    """Download audio files from provided links."""
    os.makedirs(save_path, exist_ok=True)
    downloaded: List[str] = []

    for i, link in enumerate(links):
        filename = os.path.join(save_path, f"audio_{i+1}.mp3")

        try:
            response = requests.get(link, stream=True, timeout=10)
            response.raise_for_status()

            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            downloaded.append(filename)
        except (RequestException, OSError):
            print(f"Ошибка скачивания: {link}")

    return downloaded


def create_csv(file_paths: List[str], csv_path: str) -> None:
    """Create CSV annotation file with absolute and relative paths."""
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["absolute_path", "relative_path"])

            for path in file_paths:
                writer.writerow(
                    [os.path.abspath(path), os.path.relpath(path)]
                )
    except OSError:
        print("Ошибка при создании CSV файла.")