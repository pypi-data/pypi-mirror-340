import json
import warnings
from dataclasses import asdict
from glob import glob
from os import getcwd, path
from typing import Literal, Tuple

import h5py
import numpy as np
from ReaderBOTDA.reader import Profile, Raw
from rich.progress import track

warnings.simplefilter("always", UserWarning)
warnings.simplefilter("ignore", RuntimeWarning)


class NoFilesSelected(UserWarning):
    def __init__(self, folder, message="No file found in folder"):
        self.message = f"{message}: {folder}"
        super().__init__(self.message)

    def __str__(self):
        return repr(self.message)


class FolderNotFound(UserWarning):
    def __init__(self, folder, message="Folder not found"):
        self.message = f"{message}: {folder}"
        super().__init__(self.message)

    def __str__(self):
        return repr(self.message)


def create_dataset_for_append(
    parent,
    dataset_name: str,
    first_data,
    columns,
    dtype: str,
    compression: bool = False,
):
    compression_method = "gzip" if compression else None
    return parent.create_dataset(
        dataset_name,
        data=first_data,
        dtype=dtype,
        maxshape=(None, columns),
        compression=compression_method,
    )


def append_to_dataset(dataset, data):
    rows_to_add = len(data)
    dataset.resize(dataset.shape[0] + rows_to_add, axis=0)
    dataset[-rows_to_add:, :] = data
    return dataset


def calc_statistics(file_h5):
    with h5py.File(file_h5, "r+", track_order=True) as f:
        temp = f["data"]["bfs"][:]
        BFSmean = (temp.mean(axis=0),)
        BFSstd = (temp.std(axis=0),)

        temp = f["data"]["max_gain"][:]
        MaxGainMean = (temp.mean(axis=0),)
        MaxGainStd = (temp.std(axis=0),)

        stat_grp = f.create_group("statistics")
        stat_bfs_grp = stat_grp.create_group("bfs")
        stat_bfs_grp.create_dataset("mean", data=BFSmean, dtype="f4").attrs[
            "unit"
        ] = "MHz"
        stat_bfs_grp.create_dataset("std", data=BFSstd, dtype="f4").attrs[
            "unit"
        ] = "MHz"

        stat_max_grp = stat_grp.create_group("max_gain")
        stat_max_grp.create_dataset("mean", data=MaxGainMean, dtype="f4").attrs[
            "unit"
        ] = "Volts"
        stat_max_grp.create_dataset("std", data=MaxGainStd, dtype="f4").attrs[
            "unit"
        ] = "Volts"


def calcCorrelations(
    matrice,
    reference: Literal["first", "previous"] = "previous",
    range: Tuple[float, float] = None,
) -> np.array:
    correlations = np.corrcoef(
        matrice[:, range[0] : range[1]] if range else matrice, rowvar=True
    )

    if reference == "first":
        return correlations[0, :]

    indici = np.arange(1, np.shape(correlations)[0])
    return np.insert(correlations[indici, indici - 1], 0, 1)


def calc_correlations(file_h5, range: Tuple[int, int] = None):
    with h5py.File(file_h5, "r+", track_order=True) as f:
        bfs = f["data"]["bfs"][:]
        max_gain = f["data"]["max_gain"][:]

        corr_grp = f.create_group("correlations")
        corr_bfs_grp = corr_grp.create_group("bfs")
        corr_bfs_grp.create_dataset(
            "first",
            data=calcCorrelations(bfs, reference="first", range=range),
            dtype="f4",
        )
        corr_bfs_grp.create_dataset(
            "previous",
            data=calcCorrelations(bfs, reference="previous", range=range),
            dtype="f4",
        )

        corr_max_grp = corr_grp.create_group("max_gain")
        corr_max_grp.create_dataset(
            "first", data=calcCorrelations(max_gain, reference="first"), dtype="f4"
        )
        corr_max_grp.create_dataset(
            "previous",
            data=calcCorrelations(max_gain, reference="previous"),
            dtype="f4",
        )


def load_profile_export_h5(
    filename: str,
    folder: str = None,
    statistics: bool = True,
    correlations: bool = True,
    range: Tuple[int, int] = None,
    compression: bool = True,
):
    """Carica tutti i json profile in una cartella e li converte in un unico file hdf5."""
    if not folder:
        folder = getcwd()

    if not path.isdir(folder):
        return FolderNotFound(folder=folder)

    filelist = glob(path.join(folder, "*.json"))
    if len(filelist) == 0:
        return NoFilesSelected(folder=folder)
    n_measures_per_write = 20
    with h5py.File(filename, "w", track_order=True) as f:
        timestamps = list()
        first_write = True
        number_of_files = len(filelist)
        for i, file in enumerate(
            track(filelist, description="Converting profiles...")
        ):  # [:n_measures_per_write * 50]:
            temp = Profile(filename=file)
            timestamps.append(temp.timestamp)
            try:
                BFS = np.row_stack((BFS, temp.BFS))
                MaxGain = np.row_stack((MaxGain, temp.MaxGain))
            except NameError:
                BFS = np.transpose(temp.BFS)
                MaxGain = np.transpose(temp.MaxGain)

            if np.shape(BFS)[0] == n_measures_per_write or i == number_of_files - 1:
                temp_timestamps = [np.datetime64(i).astype("<i8") for i in timestamps]
                if first_write:
                    f.attrs["folder"] = folder
                    f.attrs["sw_version"] = temp.sw_version
                    f.attrs["settings"] = json.dumps(asdict(temp.settings))
                    f.attrs["spatial_resolution"] = temp.spatialResolution
                    f.attrs["first_measure_utc"] = timestamps[0].strftime(
                        "%Y-%m-%d, %H:%M:%S.%f"
                    )
                    pos_set = f.create_dataset(
                        "position", data=temp.position, dtype="f8"
                    )
                    pos_set.make_scale("position (m)")

                    data_grp = f.create_group("data")
                    time_set = data_grp.create_dataset(
                        "timestamps",
                        data=temp_timestamps,
                        dtype="<i8",
                        maxshape=(None,),
                        compression=compression,
                    )
                    time_set.dims[0].label = "UTC Epochtime (us)"
                    bfs_set = create_dataset_for_append(
                        data_grp,
                        "bfs",
                        BFS,
                        np.shape(BFS)[1],
                        "f4",
                        compression=compression,
                    )
                    bfs_set.attrs["unit"] = "MHz"
                    bfs_set.dims[0].label = "Time"
                    bfs_set.dims[1].label = "Position"
                    bfs_set.dims[1].attach_scale(pos_set)
                    max_gain_set = create_dataset_for_append(
                        data_grp,
                        "max_gain",
                        MaxGain,
                        np.shape(MaxGain)[1],
                        "f4",
                        compression=compression,
                    )
                    max_gain_set.attrs["unit"] = "Volts"
                    max_gain_set.dims[0].label = "Time"
                    max_gain_set.dims[1].label = "Position"
                    first_write = False
                else:
                    time_set.resize(time_set.shape[0] + len(temp_timestamps), axis=0)
                    time_set[-len(temp_timestamps) :] = temp_timestamps
                    append_to_dataset(bfs_set, BFS)
                    append_to_dataset(max_gain_set, MaxGain)

                f.attrs["last_measure_utc"] = timestamps[-1].strftime(
                    "%Y-%m-%d, %H:%M:%S.%f"
                )
                del BFS, MaxGain
                timestamps = list()
            # bar.next()

    if statistics:
        calc_statistics(filename)
    if correlations:
        calc_correlations(filename, range=range)


def load_raw_export_h5(filename: str, folder: str = None, compression: bool = True):
    """Carica tutti i json matrix in una cartella e li converte in un unico file hdf5."""
    if not folder:
        folder = getcwd()

    if not path.isdir(folder):
        return FolderNotFound(folder=folder)

    filelist = glob(path.join(folder, "*.json"))
    if len(filelist) == 0:
        return NoFilesSelected(folder=folder)
    n_measures_per_write = 20
    with h5py.File(filename, "w", track_order=True) as f:
        compression_method = "gzip" if compression else None
        timestamps = list()
        raw = list()
        residuo = list()
        first_write = True
        number_of_files = len(filelist)

        for i, file in enumerate(track(filelist, description="Converting matrixes...")):
            temp = Raw(filename=file)
            timestamps.append(temp.timestamp)
            raw.append(temp.BGS)
            residuo.append(temp.residuo)

            if len(raw) == n_measures_per_write or i == number_of_files - 1:
                temp_timestamps = [np.datetime64(i).astype("<i8") for i in timestamps]
                if first_write:
                    f.attrs["folder"] = folder
                    f.attrs["sw_version"] = "1.1.0.10"
                    f.attrs["settings"] = json.dumps(asdict(temp.settings))
                    f.attrs["spatial_resolution"] = temp.spatialResolution
                    f.attrs["first_measure_utc"] = timestamps[0].strftime(
                        "%Y-%m-%d, %H:%M:%S.%f"
                    )
                    pos_set = f.create_dataset(
                        "position",
                        data=temp.position,
                        dtype="f8",
                        compression=compression_method,
                    )
                    pos_set.attrs["unit"] = "m"
                    pos_set.make_scale("position (m)")
                    freq_set = f.create_dataset(
                        "frequency",
                        data=temp.frequency,
                        dtype="f4",
                        compression=compression_method,
                    )
                    freq_set.attrs["unit"] = "MHz"
                    freq_set.make_scale("frequency (MHz)")

                    _, n_pos, n_freq = np.shape(raw)
                    data_grp = f.create_group("data")
                    temp_timestamps = [
                        np.datetime64(i).astype("<i8") for i in timestamps
                    ]
                    time_set = data_grp.create_dataset(
                        "timestamps",
                        data=temp_timestamps,
                        dtype="<i8",
                        maxshape=(None,),
                        compression=compression_method,
                    )
                    time_set.dims[0].label = "UTC Epochtime (us)"
                    raw_set = data_grp.create_dataset(
                        "raw",
                        data=raw,
                        dtype="f4",
                        maxshape=(None, n_pos, n_freq),
                        compression=compression_method,
                    )
                    raw_set.attrs["unit"] = "Volts"
                    raw_set.dims[0].label = "Time"
                    raw_set.dims[1].label = "Frequency"
                    raw_set.dims[2].label = "Position"
                    raw_set.dims[2].attach_scale(pos_set)
                    raw_set.dims[1].attach_scale(freq_set)
                    residuo_set = create_dataset_for_append(
                        data_grp,
                        "residuo",
                        residuo,
                        np.shape(residuo)[1],
                        "f4",
                        compression=compression,
                    )
                    residuo_set.attrs["unit"] = "Volts"
                    residuo_set.dims[0].label = "Time"
                    residuo_set.dims[1].label = "Frequency"
                    residuo_set.dims[1].attach_scale(freq_set)

                    first_write = False
                else:
                    time_set.resize(time_set.shape[0] + len(temp_timestamps), axis=0)
                    time_set[-len(temp_timestamps) :] = temp_timestamps

                    to_add = len(raw)
                    raw_set.resize(raw_set.shape[0] + to_add, axis=0)
                    raw_set[-to_add:, :, :] = raw

                    append_to_dataset(residuo_set, residuo)

                f.attrs["last_measure_utc"] = timestamps[-1].strftime(
                    "%Y-%m-%d, %H:%M:%S.%f"
                )
                timestamps = list()
                raw = list()
                residuo = list()
            # bar.next()
