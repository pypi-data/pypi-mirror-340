from os import getcwd, listdir, path
from typing import Optional, Tuple

import typer
from rich import print

from ConverterBOTDA.batch import run_batch_conversion
from ConverterBOTDA.functions import load_profile_export_h5, load_raw_export_h5
from ConverterBOTDA.split import split_raw_file, split_profile_file, find_type

app = typer.Typer(
    name="BOTDA Converter", short_help="Cohaerentia BOTDA json converter to h5."
)


@app.callback(invoke_without_command=True)
def base(
    filename: Optional[str] = None,  # | PathLike,
    folder: Optional[str] = None,  # | PathLike,
    range: Optional[Tuple[int, int]] = (None, None),
    statistics: Optional[bool] = True,
    correlations: Optional[bool] = True,
):
    if not folder:
        folder = getcwd()

    if not filename:
        filename = ""
    else:
        filename = filename + "_"
    profile_filename = filename + "profile.h5"
    raw_filename = filename + "raw.h5"

    if "rawarray" in listdir(folder):
        load_profile_export_h5(
            folder=path.join(folder, "rawarray"),
            filename=profile_filename,
            range=range,
            statistics=statistics,
            correlations=correlations,
        )

    if "rawmatrix" in listdir(folder):
        load_raw_export_h5(folder=path.join(folder, "rawmatrix"), filename=raw_filename)


@app.command("profile")
def profile_export_h5(
    filename: str,  # | PathLike,
    folder: Optional[str] = None,  # | PathLike,
    range: Optional[Tuple[int, int]] = (None, None),
    statistics: Optional[bool] = True,
    correlations: Optional[bool] = True,
):
    if not folder:
        folder = getcwd()
        if "rawarray" in listdir(folder):
            folder = path.join(folder, "rawarray")

    load_profile_export_h5(
        folder=folder,
        filename=filename,
        range=range,
        statistics=statistics,
        correlations=correlations,
    )


@app.command("raw")
def raw_export_h5(
    filename: str,  # | PathLike
    folder: Optional[str] = None,
):  # | PathLike):
    if not folder:
        folder = getcwd()
        if "rawmatrix" in listdir(folder):
            folder = path.join(folder, "rawmatrix")

    load_raw_export_h5(folder=folder, filename=filename)


@app.command("batch")
def batch_conversion(batch_info_filename: str):  # | PathLike):
    run_batch_conversion(batch_info=batch_info_filename)


@app.command("split")
def split(filename: str, size: Optional[int] = 100):
    """Split h5 file into smaller files, of <size> megabytes."""
    type = find_type(file=filename)
    if type == "raw":
        split_raw_file(file=filename, size_megabytes=size)
    else:
        split_profile_file(file=filename, size_megabytes=size)


@app.command("merge")
def merge(filename: str):
    """Merge multiple h5 files with same prefix in a folder into a single bigger file."""
    print("🚧 [yellow]Under development[/yellow] 🚧")


if __name__ == "__main__":
    app()
