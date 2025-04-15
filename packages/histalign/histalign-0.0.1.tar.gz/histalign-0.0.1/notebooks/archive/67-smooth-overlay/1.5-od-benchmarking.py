# SPDX-FileCopyrightText: 2025-present Olivier Delrée <olivierdelree@protonmail.com>
#
# SPDX-License-Identifier: MIT

import os
from pathlib import Path
import psutil
import sys
from time import perf_counter

import h5py
import nrrd

from histalign.backend.ccf.downloads import download_annotation_volume
from histalign.backend.ccf.paths import get_annotation_path
from histalign.backend.models import Resolution


def benchmark(resolution: Resolution) -> None:
    nrrd_path = get_annotation_path(resolution)
    h5_uncompressed_path = f"annotation_{resolution.value}.h5"
    h5_compressed_path = f"annotation_{resolution.value}.gzip.h5"

    process = psutil.Process()

    if not os.path.exists(nrrd_path):
        start_time = perf_counter()
        download_annotation_volume(resolution)
        print(f"Downloading NRRD file took: {perf_counter() - start_time:.2f} seconds.")

    memory_usage = process.memory_info().rss
    start_time = perf_counter()
    a, b = nrrd.read(nrrd_path)
    del b
    print(f"NRRD file size: {compute_file_size(nrrd_path)}")
    print(
        f"Loading NRRD file at resolution {resolution.value} took: {perf_counter() - start_time:.2f} seconds."
    )
    print(
        f"Memory usage: {compute_size(process.memory_info().rss - memory_usage)}",
        end="\n\n",
    )

    start_time = perf_counter()
    with h5py.File(h5_uncompressed_path, "w") as handle:
        handle.create_dataset("data", data=a)
    print(
        f"Saving to uncompressed HDF5 file took: {perf_counter() - start_time:.2f} seconds."
    )
    print(f"Created file size: {compute_file_size(h5_uncompressed_path)}")

    del a
    memory_usage = process.memory_info().rss
    start_time = perf_counter()
    with h5py.File(h5_uncompressed_path) as handle:
        a = handle["data"][:]
    print(
        f"Loading uncompressed HDF5 file took: {perf_counter() - start_time:.2f} seconds."
    )
    print(
        f"Memory usage: {compute_size(process.memory_info().rss - memory_usage)}",
        end="\n\n",
    )

    start_time = perf_counter()
    with h5py.File(h5_compressed_path, "w") as handle:
        handle.create_dataset("data", data=a, compression="gzip")
    print(
        f"Saving to compressed HDF5 file took: {perf_counter() - start_time:.2f} seconds."
    )
    print(f"Created file size: {compute_file_size(h5_compressed_path)}")

    del a
    memory_usage = process.memory_info().rss
    start_time = perf_counter()
    with h5py.File(h5_compressed_path) as handle:
        a = handle["data"][:]
    print(
        f"Loading compressed HDF5 file took: {perf_counter() - start_time:.2f} seconds."
    )
    print(f"Memory usage: {compute_size(process.memory_info().rss - memory_usage)}")

    del a

    os.remove(h5_uncompressed_path)
    os.remove(h5_compressed_path)


def compute_size(n_bytes: int) -> str:
    n_gib, n_bytes = divmod(n_bytes, (1024**3))
    n_mib, n_bytes = divmod(n_bytes, (1024**2))
    n_kib, n_bytes = divmod(n_bytes, (1024**1))

    return f"{n_gib} GiB - {n_mib} MiB - {n_kib} KiB - {n_bytes} B"


def compute_file_size(file_path: str | Path) -> str:
    return compute_size(os.stat(file_path).st_size)


if __name__ == "__main__":
    if len(sys.argv[1:]) != 1:
        print("Invalid number of arguments.")
        exit()

    try:
        resolution = Resolution(int(sys.argv[1]))
    except ValueError:
        print("Invalid resolution.")
        exit()

    benchmark(resolution)
