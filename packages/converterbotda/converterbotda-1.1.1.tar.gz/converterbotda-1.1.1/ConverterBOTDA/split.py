from datetime import datetime
from glob import glob
from math import ceil
from os import path
from time import strftime

import h5py
import numpy as np
from rich.progress import track


def find_type(file) -> str:
    with h5py.File(file, "r") as f:
        try:
            _ = f["data"]["bfs"]
            return "profile"
        except KeyError:
            return "raw"


def split_raw_file(file: str, size_megabytes: float = 100):
    bytes_per_sample = 4
    compression_method = "gzip"

    with h5py.File(file, "r") as source:
        raw_shape = source["data"]["raw"].shape
        mb_single_raw = (
            (raw_shape[1] * raw_shape[2] + raw_shape[1])
            * bytes_per_sample
            / (1024 * 1024)
        )
        measures_per_files = ceil(size_megabytes / mb_single_raw)
        number_files = ceil(raw_shape[0] / measures_per_files)

        for i in track(range(number_files), description=f"Splitting {file}..."):
            first_measure = i * measures_per_files
            last_measure = first_measure + measures_per_files

            target_filename = (
                path.splitext(file)[0] + f"_{i:03d}" + path.splitext(file)[1]
            )
            with h5py.File(target_filename, "w", track_order=True) as target:
                target.attrs["folder"] = source.attrs["folder"]
                target.attrs["sw_version"] = source.attrs["sw_version"]
                target.attrs["settings"] = source.attrs["settings"]
                target.attrs["spatial_resolution"] = source.attrs["spatial_resolution"]
                target.attrs["first_measure_utc"] = datetime.fromtimestamp(
                    source["data"]["timestamps"][first_measure] / 1e6
                ).strftime("%Y-%m-%d, %H:%M:%S.%f")

                target.attrs["last_measure_utc"] = datetime.fromtimestamp(
                    source["data"]["timestamps"][
                        min([last_measure - 1, raw_shape[0] - 1])
                    ]
                    / 1e6
                ).strftime("%Y-%m-%d, %H:%M:%S.%f")

                pos_set = target.create_dataset(
                    "position", data=source["position"][:], dtype="f8"
                )
                pos_set.make_scale("position (m)")

                freq_set = target.create_dataset(
                    "frequency",
                    data=source["frequency"][:],
                    dtype="f4",
                    compression=compression_method,
                )
                freq_set.attrs["unit"] = "MHz"
                freq_set.make_scale("frequency (MHz)")

                data_grp = target.create_group("data")
                time_set = data_grp.create_dataset(
                    "timestamps",
                    data=source["data"]["timestamps"][first_measure:last_measure],
                    dtype="<i8",
                    maxshape=(None,),
                    compression=compression_method,
                )
                time_set.dims[0].label = "UTC Epochtime (us)"
                raw_set = data_grp.create_dataset(
                    "raw",
                    data=source["data"]["raw"][first_measure:last_measure, :, :],
                    dtype="f4",
                    compression=compression_method,
                )
                raw_set.attrs["unit"] = "Volts"
                raw_set.dims[0].label = "Time"
                raw_set.dims[1].label = "Frequency"
                raw_set.dims[2].label = "Position"
                raw_set.dims[2].attach_scale(pos_set)
                raw_set.dims[1].attach_scale(freq_set)
                residuo_set = data_grp.create_dataset(
                    "residuo",
                    data=source["data"]["residuo"][first_measure:last_measure, :],
                    dtype="f4",
                    compression=compression_method,
                )
                residuo_set.attrs["unit"] = "Volts"
                residuo_set.dims[0].label = "Time"
                residuo_set.dims[1].label = "Frequency"
                residuo_set.dims[1].attach_scale(freq_set)


def split_profile_file(file: str, size_megabytes: float = 100):
    bytes_per_sample = 4
    compression_method = "gzip"

    with h5py.File(file, "r") as source:
        profile_shape = source["data"]["bfs"].shape
        mb_single_profile = (profile_shape[1] * 2) * bytes_per_sample / (1024 * 1024)
        measures_per_files = ceil(size_megabytes / mb_single_profile)
        number_files = ceil(profile_shape[0] / measures_per_files)

        for i in track(range(number_files), description=f"Splitting {file}..."):
            first_measure = i * measures_per_files
            last_measure = first_measure + measures_per_files

            target_filename = (
                path.splitext(file)[0] + f"_{i:03d}" + path.splitext(file)[1]
            )
            with h5py.File(target_filename, "w", track_order=True) as target:
                target.attrs["folder"] = source.attrs["folder"]
                target.attrs["sw_version"] = source.attrs["sw_version"]
                target.attrs["settings"] = source.attrs["settings"]
                target.attrs["spatial_resolution"] = source.attrs["spatial_resolution"]
                target.attrs["first_measure_utc"] = datetime.fromtimestamp(
                    source["data"]["timestamps"][first_measure] / 1e6
                ).strftime("%Y-%m-%d, %H:%M:%S.%f")

                target.attrs["last_measure_utc"] = datetime.fromtimestamp(
                    source["data"]["timestamps"][
                        min([last_measure - 1, profile_shape[0] - 1])
                    ]
                    / 1e6
                ).strftime("%Y-%m-%d, %H:%M:%S.%f")

                pos_set = target.create_dataset(
                    "position", data=source["position"][:], dtype="f8"
                )
                pos_set.make_scale("position (m)")

                data_grp = target.create_group("data")
                time_set = data_grp.create_dataset(
                    "timestamps",
                    data=source["data"]["timestamps"][first_measure:last_measure],
                    dtype="<i8",
                    maxshape=(None,),
                    compression=compression_method,
                )
                time_set.dims[0].label = "UTC Epochtime (us)"
                bfs_set = data_grp.create_dataset(
                    "bfs",
                    data=source["data"]["bfs"][first_measure:last_measure, :],
                    dtype="f4",
                    compression=compression_method,
                )
                bfs_set.attrs["unit"] = "MHz"
                bfs_set.dims[0].label = "Time"
                bfs_set.dims[1].label = "Position"
                bfs_set.dims[1].attach_scale(pos_set)
                max_gain_set = data_grp.create_dataset(
                    "max_gain",
                    data=source["data"]["max_gain"][first_measure:last_measure, :],
                    dtype="f4",
                    compression=compression_method,
                )
                max_gain_set.attrs["unit"] = "Volts"
                max_gain_set.dims[0].label = "Time"
                max_gain_set.dims[1].label = "Position"

                try:
                    stat_grp = target.create_group("statistics")
                    stat_bfs_grp = stat_grp.create_group("bfs")
                    stat_bfs_grp.create_dataset(
                        "mean", data=source["statistics"]["bfs"]["mean"], dtype="f4"
                    ).attrs["unit"] = "MHz"
                    stat_bfs_grp.create_dataset(
                        "std", data=source["statistics"]["bfs"]["std"], dtype="f4"
                    ).attrs["unit"] = "MHz"

                    stat_max_grp = stat_grp.create_group("max_gain")
                    stat_max_grp.create_dataset(
                        "mean",
                        data=source["statistics"]["max_gain"]["mean"],
                        dtype="f4",
                    ).attrs["unit"] = "Volts"
                    stat_max_grp.create_dataset(
                        "std", data=source["statistics"]["max_gain"]["std"], dtype="f4"
                    ).attrs["unit"] = "Volts"
                except KeyError:
                    pass

                try:
                    corr_grp = target.create_group("correlations")
                    corr_bfs_grp = corr_grp.create_group("bfs")
                    corr_bfs_grp.create_dataset(
                        "first",
                        data=source["correlations"]["bfs"]["first"][
                            first_measure:last_measure
                        ],
                        dtype="f4",
                    )
                    corr_bfs_grp.create_dataset(
                        "previous",
                        data=source["correlations"]["bfs"]["previous"][
                            first_measure:last_measure
                        ],
                        dtype="f4",
                    )

                    corr_max_grp = corr_grp.create_group("max_gain")
                    corr_max_grp.create_dataset(
                        "first",
                        data=source["correlations"]["max_gain"]["first"][
                            first_measure:last_measure
                        ],
                        dtype="f4",
                    )
                    corr_max_grp.create_dataset(
                        "previous",
                        data=source["correlations"]["max_gain"]["previous"][
                            first_measure:last_measure
                        ],
                        dtype="f4",
                    )
                except KeyError:
                    pass


def combine(name_prefix: str):
    """
    Combines a series of `h5` files into a single file.
    """
    file_list = glob(f"{name_prefix}*.json")

    with h5py.File(name_prefix + ".h5", "w") as combined:
        for fname in file_list:
            with h5py.File(fname, "r") as src:
                combined.attrs.update(src.attrs)
                for group in src:
                    group_id = combined.require_group(src[group].parent.name)
                    src.copy(f"/{group}", group_id, name=group)
