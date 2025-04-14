import os
import sys
from pathlib import Path

from mutagen.mp3 import MP3, HeaderNotFoundError

from minute_count.terminal_formatting import add_color
from minute_count.time_formatting import format_time


def _generate_overview(path: Path, seconds: float, seconds_precision):
    # file_name = _last_part(path)
    # print(path)
    print(f"{_highlight_path_end(path)}: {add_color(2, format_time(seconds, seconds_precision))}")


def _highlight_path_end(path: Path):
    path = str(path)
    sep = os.sep
    split = path.rsplit(sep, 1)

    if len(split) == 1:
        return add_color(3, split[0])
    else:
        return f"{split[0]}{sep}{add_color(3, split[1])}"


def _last_part(path: Path) -> str:
    parts = path.absolute().parts
    try:
        return parts[len(parts) - 1]
    except IndexError:
        print(f"Index {len(parts) - 1} is out of bounds for {parts} with length {len(parts)}")
        sys.exit(-1)


def minute_overview(path: Path, recursive: bool = True, show_output: bool = False, show_for_files: bool = False,
                    count_hidden: bool = False, live_update: bool = True, seconds_precision: bool = True,
                    minute_offset: float = 0) -> int:
    # print(path)

    if not show_output:
        show_for_files = False

    if path.is_dir():
        sigma = 0
        for file_name in os.listdir(path):
            if not count_hidden and file_name[0] == ".":
                continue

            sigma += minute_overview(path / file_name, recursive, recursive and show_output, show_for_files,
                                     live_update, seconds_precision,
                                     minute_offset + sigma)

        if show_output:
            _generate_overview(path, sigma, seconds_precision)

        return sigma
    else:
        if not str(path).endswith(".mp3"):
            return 0

        try:
            audio_file = MP3(path)
        except HeaderNotFoundError:
            return 0

        seconds = audio_file.info.length

        if show_for_files:
            _generate_overview(path, seconds, seconds_precision)

        return seconds
