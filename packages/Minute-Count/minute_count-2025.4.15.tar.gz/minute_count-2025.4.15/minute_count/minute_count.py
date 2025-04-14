import os
from pathlib import Path

from mutagen.mp3 import MP3, HeaderNotFoundError

from minute_count.terminal_formatting import add_color
from minute_count.time_formatting import format_time


def _generate_overview(path: Path, seconds: float, indent: int, seconds_precision):
    file_name = os.path.basename(path)
    print(" " * indent + f"{add_color(2, file_name)}: {format_time(seconds, seconds_precision)}")

def minute_overview(path: Path, recursive: bool = True, show_output: bool = False, show_for_files: bool = False,
                    live_update: bool = True, seconds_precision: bool = True,
                    indent_level: int = 0, minute_offset: float = 0) -> int:
    if not show_output:
        show_for_files = False

    if path.is_dir():
        sigma = 0
        for file_name in os.listdir(path):
            sigma += minute_overview(path / file_name, recursive, recursive and show_output, show_for_files,
                                     live_update, seconds_precision, indent_level + len(os.path.basename(path)),
                                     minute_offset + sigma)

            if show_output:
                _generate_overview(path, sigma, indent_level, seconds_precision)

        return sigma
    else:
        try:
            audio_file = MP3(path)
        except HeaderNotFoundError:
            return 0

        seconds = audio_file.info.length

        if show_for_files:
            _generate_overview(path, seconds, indent_level, seconds_precision)

        return seconds