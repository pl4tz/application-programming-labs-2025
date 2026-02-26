"""Module for collecting audio links from Mixkit website."""

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
        minutes, seconds = text.strip().split(":")
        return int(minutes) * 60 + int(seconds)
    except (ValueError, AttributeError):
        return 0


def collect_audio_links(min_duration: int, needed_count: int) -> List[str]:
    """Collect audio links filtered by minimum duration."""
    headers = {"User-Agent": "Mozilla/5.0"}

    categories = CATEGORIES[:]
    random.shuffle(categories)

    collected: List[str] = []

    for category in categories:
        if len(collected) >= needed_count:
            break

        url = BASE_URL + category + "/"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except RequestException:
            print(f"Ошибка запроса для категории {category}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        audio_blocks = soup.find_all("div", {"data-test-id": "audio-player"})
        duration_blocks = soup.find_all("div", {"data-test-id": "duration"})

        for block, duration_block in zip(audio_blocks, duration_blocks):
            seconds = parse_duration(duration_block.text)

            if seconds > min_duration:
                link = block.get("data-audio-player-preview-url-value")

                if link and link.endswith(".mp3") and link not in collected:
                    collected.append(link)

        if len(collected) >= needed_count:
            break

    return collected[:needed_count]