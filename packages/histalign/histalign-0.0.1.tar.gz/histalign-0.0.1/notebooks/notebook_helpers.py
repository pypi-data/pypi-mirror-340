# SPDX-FileCopyrightText: 2024-present Olivier Delrée <olivierdelree@protonmail.com>
#
# SPDX-License-Identifier: MIT

from itertools import product
import json
import logging
from pathlib import Path
from typing import Any, Callable, Iterable, Literal, Optional

import cv2
from dask.distributed import Client
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
import vedo

from histalign.backend.ccf.downloads import download_structure_mask
from histalign.backend.ccf.paths import get_structure_mask_path
from histalign.backend.io import (
    load_image,
    load_volume,
)
from histalign.backend.models import (
    AlignmentSettings,
    ProjectSettings,
    Resolution,
)
from histalign.backend.registration import Registrator

_client = None

vedo.settings.default_backend = "vtk"

KIBIBYTE = 1024
MEBIBYTE = KIBIBYTE * 1024
GIBIBYTE = MEBIBYTE * 1024

logging.lastResort.setLevel(1000)

coronal_camera = dict(
    position=[5, 0, 0],
    focal_point=[0, 0, 0],
    viewup=(0, -1, 0),
)
horizontal_camera = dict(
    position=[0, -5, 0],
    focal_point=[0, 0, 0],
    viewup=(-1, 0, 0),
)
sagittal_camera = dict(
    position=[0, 0, -5],
    focal_point=[0, 0, 0],
    viewup=(0, -1, 0),
)

axes = [
    vedo.Arrow(end_pt=(1, 0, 0), c="red", s=0.001),
    vedo.Arrow(end_pt=(0, 1, 0), c="yellow", s=0.001),
    vedo.Arrow(end_pt=(0, 0, 1), c="blue", s=0.001),
]


def x_axis() -> vedo.Arrow:
    return axes[0]


def y_axis() -> vedo.Arrow:
    return axes[1]


def z_axis() -> vedo.Arrow:
    return axes[2]


def update_cameras(volume_shape: tuple[int, int, int]) -> None:
    coronal_camera["position"] = (np.array(volume_shape) // 2).tolist()
    coronal_camera["focal_point"] = coronal_camera["position"].copy()
    coronal_camera["position"][0] += volume_shape[0] * 3
    horizontal_camera["position"] = (np.array(volume_shape) // 2).tolist()
    horizontal_camera["focal_point"] = horizontal_camera["position"].copy()
    horizontal_camera["position"][1] -= volume_shape[1] * 5
    sagittal_camera["position"] = (np.array(volume_shape) // 2).tolist()
    sagittal_camera["focal_point"] = sagittal_camera["position"].copy()
    sagittal_camera["position"][2] -= volume_shape[2] * 3


def update_axes(volume_shape: tuple[int, int, int]) -> None:
    global axes

    axes[0] = vedo.Arrow(
        end_pt=(volume_shape[0], 0, 0),
        c=x_axis().color(),
        s=0.001 * volume_shape[0],
    )

    axes[1] = vedo.Arrow(
        end_pt=(0, volume_shape[1], 0),
        c=y_axis().color(),
        s=0.001 * volume_shape[1],
    )

    axes[2] = vedo.Arrow(
        end_pt=(0, 0, volume_shape[2]),
        c=z_axis().color(),
        s=0.001 * volume_shape[2],
    )


def set_logging_level(level: int | str) -> None:
    _root_logger.setLevel(level)


def dask_client() -> None:
    global _client

    if _client is None:
        _client = Client()
    print(_client.dashboard_link)


# def load_alignment_settings(path: Path) -> AlignmentSettings:
#     with open(path) as handle:
#         return AlignmentSettings(**json.load(handle))


def load_project_settings(path: Path) -> ProjectSettings:
    with open(path) as handle:
        return ProjectSettings(**json.load(handle)["project_settings"])


def show(
    volumes: vedo.CommonVisual | list[vedo.CommonVisual] | dict[str, vedo.CommonVisual],
    interactive: bool = True,
    n: int = 1,
    camera: Optional[dict[str, Any]] = None,
) -> None:
    if isinstance(volumes, vedo.CommonVisual):
        volumes = [volumes]
    if isinstance(volumes, list):
        volumes = {f"NO_TITLE{i}": volume for i, volume in enumerate(volumes)}

    n = min(n, len(volumes))  # Don't add extra, empty renderers

    plotter = vedo.Plotter(N=n, axes=3, interactive=interactive)
    for i in range(len(volumes)):
        n_index = i % n

        title = list(volumes.keys())[i]
        if not title.startswith("NO_TITLE"):
            plotter.add(vedo.Text2D(title, pos="top-center"), at=n_index)

        plotter.add(volumes[title], at=n_index)
        plotter.at(n_index).add_global_axes(3)
    plotter.show(camera=camera)


def imshow(
    image: np.ndarray,
    cmap: Optional[str] = None,
    title: str = "",
    colorbar: bool = False,
    full_range: bool = False,
    vmin: Optional[int | float] = None,
    vmax: Optional[int | float] = None,
    figsize: Optional[tuple[int, int]] = None,
    tight: bool = True,
) -> None:
    figure, axes = plt.subplots(figsize=figsize)

    if full_range:
        try:
            vmin = np.iinfo(image.dtype).min
        except ValueError:
            vmin = np.finfo(image.dtype).min
        try:
            vmax = np.iinfo(image.dtype).max
        except ValueError:
            vmax = np.finfo(image.dtype).max

    image = axes.imshow(image, cmap=cmap, vmin=vmin, vmax=vmax)
    axes.axis(False)

    if title:
        figure.suptitle(title)
    if colorbar:
        plt.colorbar(image, ax=axes)

    if tight:
        plt.tight_layout()
    plt.show()


def hist(
    values: np.ndarray, bins: int = 10, log: bool = False, title: str = ""
) -> None:
    if title:
        plt.suptitle(title)
    plt.hist(values, bins=bins, log=log)
    plt.show()


def gridshow(
    x_coordinates: Iterable[int] | np.ndarray, y_coordinates: Iterable[int] | np.ndarray
) -> None:
    plt.plot(x_coordinates, y_coordinates, "ko", linestyle="none")
    plt.show()


def forward_register(
    image: np.ndarray, alignment_settings: AlignmentSettings
) -> np.ndarray:
    registrator = Registrator(True, True)
    return registrator.get_forwarded_image(image, alignment_settings)


def construct_cardboard_box(shape: tuple[int, int, int], value: int = -1) -> np.ndarray:
    array = np.zeros(shape=shape, dtype=np.uint8)

    draw_cardboard_box(array, value)

    return array


def draw_cardboard_box(array: np.ndarray, value: int = -1) -> None:
    if value == -1:
        value = np.iinfo(array.dtype).max

    for i in range(3):
        slice_: list[int | slice] = [
            slice(None, None, None),
        ] * 3
        slice_[i] = 0
        array[tuple(slice_)] = value

        slice_: list[int | slice] = [
            slice(None, None, None),
        ] * 3
        slice_[i] = array.shape[i] - 1
        array[tuple(slice_)] = value


def construct_array_skeleton(
    shape: tuple[int, int, int], width: int = 1, value: int = -1
) -> np.ndarray:
    array = np.zeros(shape=shape, dtype=np.uint8)

    draw_array_skeleton(array, width, value)

    return array


def draw_array_skeleton(array: np.ndarray, width: int = 1, value: int = -1) -> None:
    if value == -1:
        try:
            value = np.iinfo(array.dtype).max
        except ValueError:
            value = np.finfo(array.dtype).max

    for axis in array.shape:
        width = min(width, axis)

    for i in range(3):
        remaining_axes = list(range(3))
        remaining_axes.remove(i)

        slice_: list[int | slice] = [
            slice(0, width),
        ] * 3
        slice_[i] = slice(None, None, None)
        array[tuple(slice_)] = value

        slice_ = [
            slice(0, width),
        ] * 3
        slice_[remaining_axes[0]] = slice(
            array.shape[remaining_axes[0]] - 1 - width,
            array.shape[remaining_axes[0]] - 1,
        )
        slice_[i] = slice(None, None, None)
        array[tuple(slice_)] = value

        slice_ = [
            slice(0, width),
        ] * 3
        slice_[remaining_axes[1]] = slice(
            array.shape[remaining_axes[1]] - 1 - width,
            array.shape[remaining_axes[1]] - 1,
        )
        slice_[i] = slice(None, None, None)
        array[tuple(slice_)] = value

        slice_ = [
            slice(0, width),
        ] * 3
        slice_[remaining_axes[0]] = slice(
            array.shape[remaining_axes[0]] - 1 - width,
            array.shape[remaining_axes[0]] - 1,
        )
        slice_[remaining_axes[1]] = slice(
            array.shape[remaining_axes[1]] - 1 - width,
            array.shape[remaining_axes[1]] - 1,
        )
        slice_[i] = slice(None, None, None)
        array[tuple(slice_)] = value


def print_array_size(array: np.ndarray) -> None:
    print_size_from_bytes(array.nbytes)


def print_size_from_bytes(
    nbytes: int,
    system: Literal["decimal", "binary"] = "binary",
) -> None:
    if system not in ["decimal", "binary"]:
        raise ValueError("System should be one of decimal or binary")

    base = 1000 if system == "decimal" else 1024

    K = base
    M = K * base
    G = M * base

    calculation_nbytes = nbytes
    ngibibytes, calculation_nbytes = divmod(calculation_nbytes, G)
    nmebibytes, calculation_nbytes = divmod(calculation_nbytes, M)
    nkibibytes, calculation_nbytes = divmod(calculation_nbytes, K)

    print(
        f"{nbytes:,}B corresponds to "
        f"{ngibibytes}G{'i' if system == 'binary' else ''}B "
        f"{nmebibytes}M{'i' if system == 'binary' else ''}B "
        f"{nkibibytes}K{'i' if system == 'binary' else ''}B "
        f"{calculation_nbytes}B"
    )


def load_structure_mask(
    structure_nme: str, resolution: int, return_raw_array: bool = True
) -> np.ndarray | vedo.Volume:
    path = get_structure_mask_path(structure_nme, Resolution(resolution))

    if not Path(path).exists():
        download_structure_mask(structure_nme, Resolution(resolution))

    return load_volume(path, return_raw_array=return_raw_array)


def get_cmap(
    volume: vedo.Volume,
    cmap: str = "grey",
    alpha: Optional[list[int]] = None,
    vmin: Optional[int] = None,
    vmax: Optional[int] = None,
) -> dict[str, Any]:
    if alpha is None:
        alpha = [0, 1]

    if vmin is None:
        vmin = volume.tonumpy().min()

    if vmax is None:
        try:
            vmax = np.iinfo(volume.tonumpy().dtype).max
        except ValueError:
            vmax = np.finfo(volume.tonumpy().dtype).max

    return {
        "c": cmap,
        "alpha": alpha,
        "vmin": vmin,
        "vmax": vmax,
    }


def min_max_scale(array: np.ndarray, dtype: Optional[np.dtype] = None) -> np.ndarray:
    if dtype is None:
        dtype = array.dtype

    integer = False
    try:
        info = np.iinfo(dtype)
        integer = True
    except ValueError:
        info = np.finfo(dtype)

    array = preprocessing.minmax_scale(array, (info.min, info.max))
    if integer:
        array = np.round(array)

    return array.astype(dtype)


def normalise(array: np.ndarray, dtype: Optional[np.dtype] = None) -> np.ndarray:
    # array_dtype = array.dtype
    #
    # array = array.astype(float)
    # array -= array.min()
    # array *= np.iinfo(array_dtype).max / array.max()
    # array = np.round(array).astype(array_dtype)
    #
    # return array

    if dtype is None:
        dtype = array.dtype

    maximum = get_dtype_max(dtype)

    array = array.astype(float)
    return (maximum * (array - np.min(array)) / np.ptp(array)).astype(dtype)


def convert_to_dtype(array: np.ndarray, dtype: np.dtype) -> np.ndarray:
    scaling = np.iinfo(dtype).max / np.iinfo(array.dtype).max
    array = array.astype(float)
    array *= scaling
    array = np.round(array)

    return array.astype(dtype)


def interpolation_function(chunk: np.ndarray, interpolator: Callable) -> np.ndarray:
    try:
        interpolated_data = interpolator(chunk)
    except np.linalg.LinAlgError:
        interpolated_data = np.zeros(shape=(chunk.shape[0],), dtype=np.float64)

    return interpolated_data


# def interpolate_sparse_3d_array(
#     array: np.ndarray,
#     reference_mask: Optional[np.ndarray] = None,
#     pre_masked: bool = False,
#     kernel: str = "multiquadric",
#     neighbours: int = 27,
#     epsilon: int = 1,
#     degree: Optional[int] = None,
#     chunk_size: Optional[int] = 1_000_000,
#     recursive: bool = False,
# ) -> np.ndarray:
#     start_time = time.perf_counter()
#
#     if reference_mask is not None and (array_shape := array.shape) != (
#         reference_shape := reference_mask.shape
#     ):
#         raise ValueError(
#             f"Array and reference mask have different shapes "
#             f"({array_shape} vs {reference_shape})."
#         )
#
#     # Mask the array if necessary
#     if reference_mask is not None and not pre_masked:
#         array = np.where(reference_mask, array, 0)
#
#     interpolated_array = array.copy()
#     interpolated_array = interpolated_array.astype(np.float64)
#
#     if reference_mask is None:
#         # Interpolate the whole grid
#         target_coordinates = tuple(
#             array.flatten().astype(int)
#             for array in np.meshgrid(
#                 np.linspace(
#                     0, interpolated_array.shape[0] - 1, interpolated_array.shape[0]
#                 ),
#                 np.linspace(
#                     0, interpolated_array.shape[1] - 1, interpolated_array.shape[1]
#                 ),
#                 np.linspace(
#                     0, interpolated_array.shape[2] - 1, interpolated_array.shape[2]
#                 ),
#                 indexing="ij",
#             )
#         )
#     else:
#         # Interpolate only non-zero coordinates of mask
#         target_coordinates = np.nonzero(reference_mask)
#     target_points = np.array(target_coordinates).T
#
#     if chunk_size is None:
#         chunk_size = target_points.shape[0]
#
#     logging.info(
#         f"Starting interpolation with parameters "
#         f"{{"
#         f"kernel: {kernel}, "
#         f"neighbours: {neighbours}, "
#         f"epsilon: {epsilon}, "
#         f"degree: {degree}, "
#         f"chunk size: {chunk_size}, "
#         f"recursive: {recursive}"
#         f"}}."
#     )
#
#     failed_chunks = []
#     previous_target_size = target_points.shape[0]
#     while True:
#         known_coordinates = np.nonzero(interpolated_array)
#         known_points = np.array(known_coordinates).T
#
#         known_values = array[known_coordinates]
#
#         interpolator = RBFInterpolator(
#             known_points,
#             known_values,
#             kernel=kernel,
#             neighbors=neighbours,
#             epsilon=epsilon,
#             degree=degree,
#         )
#
#         chunk_start = 0
#         chunk_end = chunk_size
#         chunk_index = 1
#         chunk_count = math.ceil(target_points.shape[0] / chunk_size)
#         while chunk_start < target_points.shape[0]:
#             logging.info(
#                 f"Interpolating chunk {chunk_index}/{chunk_count} "
#                 f"({chunk_index / chunk_count:.0%})."
#             )
#
#             chunk_coordinates = tuple(
#                 coordinate[chunk_start:chunk_end] for coordinate in target_coordinates
#             )
#             chunk_points = target_points[chunk_start:chunk_end]
#
#             try:
#                 interpolated_array[chunk_coordinates] = interpolator(chunk_points)
#             except np.linalg.LinAlgError:
#                 failed_chunks.append([chunk_start, chunk_end])
#                 logging.info(f"Failed to interpolate chunk {chunk_index}.")
#
#             chunk_start += chunk_size
#             chunk_end += chunk_size
#             chunk_index += 1
#
#         if not recursive or len(failed_chunks) == 0:
#             break
#
#         # Prepare the next loop
#         target_coordinates = tuple(
#             np.concatenate(
#                 [target_coordinate[start:end] for start, end in failed_chunks]
#             )
#             for target_coordinate in target_coordinates
#         )
#         target_points = np.array(target_coordinates).T
#         failed_chunks = []
#
#         # Avoid infinitely looping
#         if previous_target_size == target_points.shape[0]:
#             logging.error(
#                 f"Interpolation is not fully solvable with current combination of "
#                 f"kernel, neighbours parameter and chunk size. "
#                 f"Returning current result."
#             )
#             break
#         previous_target_size = target_points.shape[0]
#
#         logging.info(
#             f"There were {len(failed_chunks)} failed chunks of size {chunk_size}. "
#             f"Recursing with newly interpolated data."
#         )
#
#     total_time = time.perf_counter() - start_time
#     total_hours, remaining_time = divmod(total_time, 3600)
#     total_minutes, total_seconds = divmod(remaining_time, 60)
#     time_string = (
#         f"{f'{total_hours:.0f}h' if total_hours else ''}"
#         f"{f'{total_minutes:>2.0f}m' if total_minutes else ''}"
#         f"{total_seconds:>2.0f}s"
#     )
#     logging.info(f"Finished interpolation in {time_string}.")
#
#     return interpolated_array


def mask_central_circle(
    array: np.ndarray, radius: int = 10, mode: Literal["keep", "remove"] = "keep"
) -> np.ndarray:
    i_size, j_size = array.shape

    i_origins = {i_size // 2, i_size // 2 + bool(i_size % 2 == 0)}
    j_origins = {j_size // 2, j_size // 2 + bool(j_size % 2 == 0)}

    origins = list(product(i_origins, j_origins))

    for origin in origins:
        i, j = np.ogrid[
            -origin[0] : i_size - origin[0], -origin[1] : j_size - origin[1]
        ]
        mask = i**2 + j**2 <= radius**2

        array[mask] = 0

    return array


def get_center_slice(
    array: np.ndarray, i_radius: int = 100, j_radius: int = 100
) -> tuple[slice, slice]:
    center = array.shape[0] // 2, array.shape[1] // 2
    i_diameter = 2 * i_radius + 1 + int(array.shape[0] % 2 == 0)
    j_diameter = 2 * j_radius + 1 + int(array.shape[1] % 2 == 0)

    i_start = center[0] - i_radius - int(array.shape[0] % 2 == 0)
    i_end = i_start + i_diameter
    j_start = center[1] - j_radius - int(array.shape[1] % 2 == 0)
    j_end = j_start + j_diameter

    return slice(i_start, i_end), slice(j_start, j_end)


def get_center_mask(
    array: np.ndarray, i_radius: int = 100, j_radius: int = 100
) -> np.ndarray:
    i_slice, j_slice = get_center_slice(array, i_radius, j_radius)

    mask = np.zeros_like(array, dtype=bool)
    mask[i_slice, j_slice] = True

    return mask


def crop_to_center(
    array: np.ndarray, i_radius: int = 100, j_radius: int = 100
) -> np.ndarray:
    i_slice, j_slice = get_center_slice(array, i_radius, j_radius)
    cropped = array[i_slice, j_slice]

    return cropped


def get_mask_from_alignment(alignment_path: Path, structure_name: str) -> np.ndarray:
    settings = load_alignment_settings(alignment_path)

    registrator = Registrator(True, True)
    return registrator.get_reversed_image(settings, structure_name)


def preprocess(alignment_path: Path, downsampling_rate: int = 1) -> None:
    downsampling_slice = (slice(None, None, downsampling_rate),) * 2

    settings = load_alignment_settings(alignment_path)

    neun_image = load_image(settings.histology_path)[downsampling_slice]

    preprocessed_image = remove_bright_spots(neun_image)

    mask = get_mask_from_alignment(alignment_path, "root")[downsampling_slice]

    background = extract_background(neun_image, mask)
    background_average_intensity = compute_subset_mean(neun_image, 1, (2**16 - 1) // 4)
    preprocessed_image = subtract_from_array(
        preprocessed_image, background_average_intensity
    )

    preprocessed_image = np.where(mask, preprocessed_image, 0)

    mecp_path = (
        settings.histology_path.parent.parent
        / "channel2"
        / settings.histology_path.name.replace("470", "700").replace("New 1", "New 2")
    )
    mecp_image = load_image(mecp_path)[downsampling_slice]

    imshow(
        neun_image,
        title=f"NeuN ({settings.histology_path.stem})",
        vmin=0,
        vmax=preprocessed_image.max(),
        colorbar=True,
    )
    imshow(mecp_image, title="MECP2", vmin=0, vmax=preprocessed_image.max())
    imshow(background, title="Background", vmin=0, vmax=preprocessed_image.max())
    imshow(
        preprocessed_image, title="Preprocessed", vmin=0, vmax=preprocessed_image.max()
    )


def remove_bright_spots(
    image: np.ndarray, threshold: Optional[int] = None
) -> np.ndarray:
    if threshold is None:
        threshold = get_dtype_max(image.dtype) * (3 / 5)

    return np.where(image > threshold, 0, image)


def extract_background(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    return np.where(mask, 0, image)


def compute_subset_mean(array: np.ndarray, subset_range: list[int]) -> float:
    lower_range = min(subset_range)
    upper_range = max(subset_range)

    subset_array = array[(lower_range <= array) & (array <= upper_range)]
    return float(np.mean(subset_array))


def get_dtype_max(dtype: np.dtype) -> int | float:
    try:
        maximum = np.iinfo(dtype).max
    except ValueError:
        maximum = np.finfo(dtype).max

    return maximum


def subtract_from_array(array: np.ndarray, value: int | float) -> np.ndarray:
    if array.dtype not in [np.uint8, np.uint16, np.uint32]:
        raise NotImplementedError("Function only implemented on unsigned ints.")

    maximum = get_dtype_max(array.dtype)

    return np.clip(array.astype(float) - value, 0, maximum).astype(array.dtype)


def auto_contrast(image: np.ndarray, passes: int = 1) -> np.ndarray:
    """Applies the ImageJ auto-contrast algorithm

    Reference:
    https://github.com/imagej/ImageJ/blob/master/ij/plugin/frame/ContrastAdjuster.java#L815
    """
    pixel_count = np.prod(image.shape)
    limit = pixel_count / 10

    auto_threshold = 5000 / passes
    threshold = pixel_count / auto_threshold

    histogram = np.histogram(image, bins=256, range=(0, get_dtype_max(image.dtype)))
    histogram = (histogram[0], np.round(histogram[1]).astype(np.uint32))

    for i in range(256):
        count = histogram[0][i]

        if count > limit:
            count = 0

        found = count > threshold

        if found:
            break
    hmin = i

    for j in range(255, -1, -1):
        count = histogram[0][j]

        if count > limit:
            count = 0

        found = count > threshold

        if found:
            break
    hmax = j

    auto_contrasted_image = np.clip(image, histogram[1][hmin], histogram[1][hmax])
    return normalise(auto_contrasted_image)


# def compute_normal(
#     orientation: Orientation,
#     pitch: int = 0,
#     yaw: int = 0,
#     pitch_first: bool = True,
# ) -> np.ndarray:
#     """Computes the normal to the plane described by orientation and principal axes.
#
#     Note that rotations in 3D are not commutative, hence the `pitch_first` argument.
#     By default, pitch rotation if applied first.
#
#     Adapted from this StackOverflow exchange: https://math.stackexchange.com/q/2618527.
#
#     Args:
#         orientation (Orientation): Orientation to determine which axis to "look out of".
#                                    For example, given a coronal orientation, the
#                                    normal without any rotations would be (-1, 0, 0).
#         pitch (int): Angle in degree with which to raise the normal.
#         yaw (int): Angle in degrees with which to rotate around the vertical axis.
#         pitch_first (bool, optional): Whether to apply pitch before yaw.
#
#     Returns:
#         np.ndarray: The normal to the orientation plane after applying applying the
#                     rotations.
#
#     Examples:
#         Working with a sagittal orientation, the plane that is being rotated is the one
#         described by the X and Y axes. Given the way the Allen CCF is oriented, the
#         normal without any rotations is (0, 0, 1), i.e., looking out of the
#         medio-lateral axis, with the dorso-ventral axis pointing down and the
#         rostro-caudal axis pointing right.
#
#         Therefore, applying a pitch of 20 degrees tilts the plane
#         back by 20 degrees, giving us a normal with a negative Y component and a reduced
#         Z component.
#
#         > compute_normal(Orientation.SAGITTAL, pitch=20, yaw=0)
#         array([ 0.        , -0.34202014,  0.93969262])
#
#         Similarly, a 20 degrees yaw rotates to the right, giving us a positive X
#         component and a reduced Z component.
#
#         > compute_normal(Orientation.SAGITTAL, pitch=0, yaw=20)
#         array([ 0.34202014, -0.        ,  0.93969262])
#
#         And a combination of the two gives us components for all the axes.
#
#         > compute_normal(Orientation.SAGITTAL, pitch=20, yaw=20)
#         array([ 0.34202014, -0.3213938 ,  0.88302222])
#
#     See Also:
#         https://en.wikipedia.org/wiki/Aircraft_principal_axes#Principal_axes
#     """
#
#     pitch = math.radians(pitch)
#     yaw = math.radians(yaw)
#
#     match orientation:
#         case Orientation.CORONAL:
#             if pitch_first:
#                 normal = [
#                     -math.cos(yaw) * math.cos(pitch),
#                     -math.sin(pitch),
#                     math.sin(yaw) * math.cos(pitch),
#                 ]
#             else:
#                 normal = [
#                     -math.cos(pitch) * math.cos(yaw),
#                     -math.sin(pitch) * math.cos(yaw),
#                     math.sin(yaw),
#                 ]
#         case Orientation.HORIZONTAL:
#             if pitch_first:
#                 normal = [
#                     -math.sin(pitch),
#                     math.cos(yaw) * math.cos(pitch),
#                     math.sin(yaw) * math.cos(pitch),
#                 ]
#             else:
#                 normal = [
#                     -math.sin(pitch) * math.cos(yaw),
#                     math.cos(pitch) * math.cos(yaw),
#                     math.sin(yaw),
#                 ]
#         case Orientation.SAGITTAL:
#             if pitch_first:
#                 normal = [
#                     math.sin(yaw) * math.cos(pitch),
#                     -math.sin(pitch),
#                     math.cos(yaw) * math.cos(pitch),
#                 ]
#             else:
#                 normal = [
#                     math.sin(yaw),
#                     -math.sin(pitch) * math.cos(yaw),
#                     math.cos(pitch) * math.cos(yaw),
#                 ]
#         case other:
#             # Should be impossible thanks to pydantic
#             raise InvalidOrientationError(other)
#
#     return np.array(normal)


def format_list(list_: Iterable, format_: str = ">6.3f") -> str:
    return " | ".join(f"{value:{format_}}" for value in list_)


def find_contours(image: np.ndarray) -> list[np.ndarray]:
    return cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]


def draw_contours(
    contours: list[np.ndarray],
    image: np.ndarray,
    colour: tuple[int, int, int] = (255, 255, 255),
    width: int = 10,
) -> None:
    cv2.drawContours(image, contours, -1, colour, width)


def compute_largest_contour(image: np.ndarray) -> np.ndarray:
    contours = find_contours(image)
    return max(contours, key=cv2.contourArea)


# Easier to understand but 3x slower
# def closest_contour_point(point, contour):
#     distances = np.sum((contour - point) ** 2, axis=1)
#     return np.argmin(distances)


def closest_contour_point(point, contour):
    deltas = contour - point
    distances = np.einsum("ij,ij->i", deltas, deltas)
    return np.argmin(distances)


def compute_closest_contour_point(
    points: np.ndarray, points_pool: np.ndarray
) -> np.ndarray:
    return np.array(
        [points_pool[closest_contour_point(point, points_pool)] for point in points]
    )


def compute_distances_nonisometric_grid(
    points: np.ndarray, points_pool: np.ndarray, x_size: float, y_size: float
) -> np.ndarray:
    return np.array(
        [
            np.sqrt(
                ((point[0] - pool_point[0]) * x_size) ** 2
                + ((point[1] - pool_point[1]) * y_size) ** 2
            )
            for point, pool_point in zip(points, points_pool)
        ]
    )


def apply_transformation_matrix_to_contour(
    transformation_matrix: np.ndarray,
    contour: np.ndarray,
) -> np.ndarray:
    return np.array(
        [
            np.matmul(transformation_matrix, np.concatenate([point, [1]]))[:2]
            for point in contour
        ]
    )


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
