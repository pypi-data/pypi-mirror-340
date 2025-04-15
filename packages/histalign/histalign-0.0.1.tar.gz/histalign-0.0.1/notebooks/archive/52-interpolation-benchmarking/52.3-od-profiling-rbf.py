# SPDX-FileCopyrightText: 2024-present Olivier Delrée <olivierdelree@protonmail.com>
#
# SPDX-License-Identifier: MIT

from pathlib import Path
import time
from typing import Optional

import dask.array as da
import numpy as np
from scipy.interpolate import RBFInterpolator

from histalign import set_log_level, _module_logger
from histalign.backend.models import Resolution
from histalign.backend.registration.alignment import (
    build_alignment_volume,
    interpolate_sparse_3d_array,
)
from notebook_helpers import load_structure_mask

set_log_level("DEBUG")


def get_tuple_all_coordinates(array_shape: tuple[int, ...]) -> tuple[np.ndarray, ...]:
    assert max(array_shape) < 2**16 - 1, "Supported coordinate dtype is np.uint16"

    return tuple(
        array.flatten().astype(int)
        for array in np.meshgrid(
            *[
                np.linspace(0, array_shape[i] - 1, array_shape[i], dtype=np.uint16)
                for i in range(len(array_shape))
            ],
            indexing="ij",
        )
    )


def interpolate(
    array: np.ndarray, mask: Optional[np.ndarray] = None, dask: bool = False
) -> np.ndarray:
    interpolated_array = array.copy().astype(np.float64)

    known_coordinates = np.nonzero(interpolated_array)
    known_points = np.array(known_coordinates).T
    if dask:
        known_points = da.from_array(known_points)

    known_values = array[known_coordinates]
    if dask:
        known_values = da.from_array(known_values)

    interpolator = RBFInterpolator(
        known_points,
        known_values,
        kernel="multiquadric",
        neighbors=16,
        epsilon=1,
        degree=None,
    )

    def interpolation_function(chunk: np.ndarray) -> np.ndarray:
        try:
            interpolated_data = interpolator(chunk)
        except np.linalg.LinAlgError:
            interpolated_data = np.zeros(shape=(chunk.shape[0],), dtype=np.float64)

        return interpolated_data

    if mask is not None:
        target_coordinates = np.nonzero(mask)
    else:
        target_coordinates = get_tuple_all_coordinates(interpolated_array.shape)
    target_points = np.array(target_coordinates, np.uint16).T
    if dask:
        target_points = da.from_array(target_points)

    if dask:
        interpolated_array[target_coordinates] = da.map_blocks(
            interpolation_function, target_points, drop_axis=1, dtype=np.float64
        ).compute()
    else:
        interpolated_array[target_coordinates] = interpolation_function(target_points)

    return interpolated_array


if __name__ == "__main__":
    alignment_path = Path(
        "/home/ediun/git/histalign/projects/project_cortical_depth/93e6cae680"
    )

    array = build_alignment_volume(alignment_path, return_raw_array=True)
    # mask = load_structure_mask("Somatomotor areas", Resolution.MICRONS_25)

    _module_logger.debug("Started interpolation.")

    start_time = time.perf_counter()
    interpolated_array = interpolate(
        array,
        # mask,
    )
    end_time = time.perf_counter()

    _module_logger.debug(
        f"Finished interpolation (took {end_time - start_time:.0f} seconds)."
    )
