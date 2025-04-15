# SPDX-FileCopyrightText: 2025-present Olivier Delrée <olivierdelree@protonmail.com>
#
# SPDX-License-Identifier: MIT

import cv2
import numpy as np
from PIL import Image, ImageTransform
import psutil

MiB = 1024**2

matrix = np.array(
    [
        [2, 0, 1000],
        [0, 2, 1000],
    ]
).flatten()


process = psutil.Process()

initial_memory = process.memory_info().rss

image_np = np.random.randint(0, 255, (20_000, 20_000), dtype=np.uint8)

after_np_memory = process.memory_info().rss

image_pil_array = Image.fromarray(image_np)
image_pil_array.readonly = False

after_pil_array_memory_usage = process.memory_info().rss

image_pil_buffer = Image.frombuffer(
    "L", image_np.shape[::-1], image_np, "raw", "L", 0, 1
)

after_pil_buffer_memory_usage = process.memory_info().rss

transformed_image = image_pil_buffer.transform(
    image_pil_buffer.size, ImageTransform.AffineTransform(matrix)
)

after_transform_memory_usage = process.memory_info().rss

print(f"Initial memory usage: {initial_memory // MiB} MiB")
print(f"After numpy memory usage: {after_np_memory // MiB} MiB")
print(f"Difference memory usage: {(after_np_memory - initial_memory) // MiB} MiB")
print(f"After PIL array memory usage: {after_pil_array_memory_usage // MiB} MiB")
print(
    f"Difference memory usage: {(after_pil_array_memory_usage - after_np_memory) // MiB} MiB"
)
print(f"After PIL array memory usage: {after_pil_buffer_memory_usage // MiB} MiB")
print(
    f"Difference memory usage: {(after_pil_buffer_memory_usage - after_pil_array_memory_usage) // MiB} MiB"
)
print(f"After transform array memory usage: {after_transform_memory_usage // MiB} MiB")
print(
    f"Difference memory usage: {(after_transform_memory_usage - after_pil_buffer_memory_usage) // MiB} MiB"
)

image_np[10, 10] = 0

print(image_pil_array.getpixel((10, 10)))

image_pil_array.putpixel((20, 20), 0)

print(image_np[20, 20])
