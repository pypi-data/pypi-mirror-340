import json
from dataclasses import dataclass
from os import PathLike, path
from typing import List, Tuple

# from tqdm.auto import tqdm
from rich.progress import track

from .functions import load_profile_export_h5, load_raw_export_h5


@dataclass
class Entry:
    folder: str | PathLike
    range: Tuple[float, float] = None


def load_batch_info(filename: str | PathLike) -> List[Entry]:
    with open(filename, "r") as f:
        temp = json.load(f)
    return [Entry(**entry) for entry in temp["entries"]]


def run_batch_conversion(batch_info: List[Entry] | str | PathLike):
    if not isinstance(
        batch_info, List
    ):  # all(isinstance(elem, Entry) for elem in batch_info):
        batch_info = load_batch_info(batch_info)

    for entry in track(batch_info, description="Folders"):
        folder, range = entry.folder, entry.range
        load_profile_export_h5(
            folder=path.join(folder, "rawarray"),
            filename=path.join(folder, "profile.h5"),
            range=range,
        )
        load_raw_export_h5(
            folder=path.join(folder, "rawmatrix"), filename=path.join(folder, "raw.h5")
        )


if __name__ == "__main__":
    run_batch_conversion("../batch_info.json")
