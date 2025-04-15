import itertools
import math
import sys
from time import perf_counter

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTransform
import skimage


def get_transform_matrix(
    translation: tuple[int, int] = (0, 0),
    scaling: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
    shearing: tuple[float, float] = (0.0, 0.0),
    transformation_origin: tuple[int, int] = (0, 0),
) -> np.ndarray:
    matrix = np.eye(3, 3)

    # Change origin
    matrix = (
        np.array(
            [
                [1, 0, -transformation_origin[0]],
                [0, 1, -transformation_origin[1]],
                [0, 0, 1],
            ]
        )
        @ matrix
    )

    # Rotate
    matrix = (
        np.array(
            [
                [math.cos(rotation), -math.sin(rotation), 0],
                [math.sin(rotation), math.cos(rotation), 0],
                [0, 0, 1],
            ]
        )
        @ matrix
    )

    # Scale
    matrix = (
        np.array(
            [
                [scaling[0], 0, 0],
                [0, scaling[1], 0],
                [0, 0, 1],
            ]
        )
        @ matrix
    )

    # Change origin back
    matrix = (
        np.array(
            [
                [1, 0, transformation_origin[0]],
                [0, 1, transformation_origin[1]],
                [0, 0, 1],
            ]
        )
        @ matrix
    )

    # Shear
    matrix = (
        np.array(
            [
                [1, shearing[0], 0],
                [shearing[1], 1, 0],
                [0, 0, 1],
            ]
        )
        @ matrix
    )

    # Translate
    matrix = (
        np.array(
            [
                [1, 0, translation[0]],
                [0, 1, translation[1]],
                [0, 0, 1],
            ]
        )
        @ matrix
    )

    return matrix


if len(sys.argv[1:]) == 2:
    shape = (sys.argv[1], sys.argv[2])
    shape = tuple(map(int, shape))
else:
    shape = (32_000, 32_000)

print(f"Image shape: {shape}")

image = np.random.randint(0, 2**16 - 1, np.prod(shape), dtype=np.uint16).reshape(shape)

matrix = get_transform_matrix(
    translation=(
        int(np.random.randint(0, image.shape[0] - 1)),
        int(np.random.randint(0, image.shape[1])),
    ),
    scaling=(0.8, 1.6),
    rotation=math.pi / 2,
    shearing=(1.2, 0.9),
    transformation_origin=(image.shape[0] // 2, image.shape[1] // 2),
)

# OpenCV affine warping
try:
    start_time = perf_counter()
    _ = cv2.warpAffine(
        image,
        matrix[:2],
        image.shape[::-1],
        flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
    )
    print(f"OpenCV affine warping: {perf_counter() - start_time:.2f} seconds.")
except cv2.error:
    print("OpenCV affine warping: N/A")

# OpenCV perspective warping
try:
    start_time = perf_counter()
    _ = cv2.warpPerspective(
        image, matrix, image.shape[::-1], flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP
    )
    print(f"OpenCV perspective warping: {perf_counter() - start_time:.2f} seconds.")
except cv2.error:
    print("OpenCV perspective warping: N/A")

# skimage
start_time = perf_counter()
_ = skimage.transform.warp(image, matrix)
print(f"skimage warping: {perf_counter() - start_time:.2f} seconds.")

# pillow warping
initial_time = perf_counter()
image = Image.fromarray(image)

transform = ImageTransform.AffineTransform(matrix.flatten()[:6])

start_time = perf_counter()
_ = image.transform(image.size, transform)
print(
    f"pillow warping: {perf_counter() - start_time:.2f} seconds "
    f"(total: {perf_counter() - initial_time:.2f} seconds)."
)
