import os.path
from pathlib import Path
import shutil
import sys

import click
import h5py
import numpy as np

from histalign.backend.ccf.downloads import download_atlas
from histalign.backend.ccf.paths import get_atlas_path
from histalign.backend.io import load_volume
from histalign.backend.models import (
    Orientation,
    Resolution,
    VolumeSettings,
)
from histalign.backend.workspace import VolumeSlicer


@click.command
@click.option(
    "-o",
    "--orientation",
    type=str,
    required=False,
    default="coronal",
)
@click.option(
    "-r",
    "--resolution",
    type=int,
    required=False,
    default=100,
)
@click.option(
    "-c",
    "--count",
    "slices_count",
    type=int,
    required=False,
    default=40,
)
@click.option(
    "-z",
    "--z-stack-size",
    type=int,
    required=False,
    default=5,
)
@click.option(
    "-p",
    "--pitch",
    type=int,
    required=False,
    default=7,
)
@click.option(
    "-y",
    "--yaw",
    type=int,
    required=False,
    default=11,
)
def main(
    orientation: str = "coronal",
    resolution: int = 100,
    slices_count: int = 40,
    z_stack_size: int = 5,
    pitch: int = 7,
    yaw: int = 11,
) -> None:
    try:
        orientation = Orientation(orientation)
    except ValueError:
        click.echo(
            f"Could not parse '{orientation}' as a valid orientation. "
            f"Allowed values are: {' '.join(map(lambda x: x.value, iter(Orientation)))}"
        )
        exit()
    try:
        resolution = Resolution(resolution)
    except ValueError:
        click.echo(
            f"Could not parse '{resolution}' as a valid resolution. "
            f"Allowed values are: "
            f"{' '.join(map(lambda x: str(x.value), iter(Resolution)))}",
            err=True,
        )
        exit()

    root = Path(os.path.expanduser("~")) / "tmp" / "datasets" / orientation.value

    path_2d = root / "artificial_2d"
    path_3d = root / "artificial_3d"

    shutil.rmtree(root, ignore_errors=True)

    os.makedirs(path_2d / "normal", exist_ok=True)
    os.makedirs(path_2d / "rotated", exist_ok=True)
    os.makedirs(path_3d / "normal", exist_ok=True)
    os.makedirs(path_3d / "rotated", exist_ok=True)

    match resolution:
        case Resolution.MICRONS_100:
            shape = (132, 80, 114)
        case Resolution.MICRONS_50:
            shape = (264, 160, 228)
        case Resolution.MICRONS_25:
            shape = (528, 320, 456)
        case Resolution.MICRONS_10:
            shape = (130, 800, 1140)
        case _:
            raise Exception("ASSERT NOT REACHED")

    atlas_path = Path(get_atlas_path(resolution))
    if not atlas_path.exists():
        download_atlas(resolution)
    atlas = load_volume(atlas_path, return_raw_array=True)

    match orientation:
        case Orientation.CORONAL:
            indices = list(range(0, shape[0]))
        case Orientation.HORIZONTAL:
            indices = list(range(0, shape[1]))
        case Orientation.SAGITTAL:
            indices = list(range(0, shape[2]))
        case _:
            raise Exception("ASSERT NOT REACHED")

    step = len(indices) // (slices_count + 1)

    # Single-slice, non-rotated
    for i in range(slices_count):
        index = indices[step::step][i]

        image = atlas[index]

        with h5py.File(path_2d / "normal" / f"image_{index}.h5", "w") as handle:
            handle.create_dataset(data=image, name="array")

    # Z-stack, non-rotated
    for i in range(slices_count):
        index = indices[step::step][i]

        images = []
        for j in range(-(z_stack_size - 1) // 2, z_stack_size // 2):
            images.append(atlas[index])

        stack = np.stack(images)
        with h5py.File(path_3d / "normal" / f"image_{index}.h5", "w") as handle:
            handle.create_dataset(data=stack, name="array")

    # Single-slice, rotated
    for i in range(slices_count):
        index = indices[step::step][i]

        image = atlas[index]

        with h5py.File(path_2d / "rotated" / f"image_{index}.h5", "w") as handle:
            handle.create_dataset(data=image, name="array")

    # Z-stack, rotated
    for i in range(slices_count):
        index = indices[step::step][i]

        images = []
        for j in range(-(z_stack_size - 1) // 2, z_stack_size // 2):
            images.append(atlas[index])

        stack = np.stack(images)
        with h5py.File(path_3d / "rotated" / f"image_{index}.h5", "w") as handle:
            handle.create_dataset(data=stack, name="array")


if __name__ == "__main__":
    main(sys.argv[1:])
