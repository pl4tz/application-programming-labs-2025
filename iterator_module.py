"""Module containing AudioIterator class."""

import csv
import os
from typing import Iterator


class AudioIterator(Iterator[str]):
    """Iterator for audio files from CSV file or directory."""

    def __init__(self, source: str) -> None:
        if os.path.isfile(source):
            try:
                self.file = open(source, encoding="utf-8")
                self.reader = csv.reader(self.file)
                next(self.reader)
                self.mode = "csv"
            except OSError as error:
                raise ValueError("Не удалось открыть CSV файл") from error
        elif os.path.isdir(source):
            self.files = [
                os.path.join(source, f)
                for f in os.listdir(source)
                if f.endswith(".mp3")
            ]
            self.index = 0
            self.mode = "dir"
        else:
            raise ValueError("Неверный источник данных")

    def __iter__(self) -> "AudioIterator":
        """Return iterator instance."""
        return self

    def __next__(self) -> str:
        """Return next audio file path."""
        if self.mode == "csv":
            try:
                return next(self.reader)[0]
            except StopIteration:
                self.file.close()
                raise
        else:
            if self.index >= len(self.files):
                raise StopIteration
            file_path = self.files[self.index]
            self.index += 1
            return file_path