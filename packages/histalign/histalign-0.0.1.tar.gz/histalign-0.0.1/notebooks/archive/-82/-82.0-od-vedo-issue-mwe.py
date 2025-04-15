import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation
import vedo


def compute_normal(pitch: int, yaw: int) -> np.ndarray:
    normal = [-1, 0, 0]
    rotation = Rotation.from_euler("ZY", [pitch, yaw], degrees=True)

    return rotation.apply(normal)


def slice_image(volume: vedo.Volume, offset: int, pitch: int, yaw: int) -> np.ndarray:
    slice_mesh = volume.slice_plane(
        origin=volume.center() + [-offset, 0, 0],
        normal=compute_normal(pitch, yaw),
    )

    # I would also normally rotate the image by pitch so that the intersection line
    # points up on the image.
    return slice_mesh.pointdata["ImageScalars"].reshape(slice_mesh.metadata["shape"])


offset = 50
pitch = 10
yaw = 40

array = np.zeros(shape=(200, 150, 180), dtype=np.uint8)
array[..., (array.shape[2] - 1) // 2] = 1

volume = vedo.Volume(array)

slice_plane = vedo.Plane(
    pos=volume.center() + [-offset, 0, 0],
    normal=compute_normal(pitch, yaw),
    s=(array.shape[2], array.shape[1]),
)

camera = dict(
    position=volume.center() + [500, 0, 0],
    focal_point=volume.center(),
    viewup=(0, -1, 0),
)

plotter = vedo.Plotter(axes=3)
plotter += [volume, slice_plane]
plotter.show(camera=camera)

image = slice_image(volume, offset, pitch, yaw)

# Show the center of the image
image[(image.shape[0] - 1) // 2] = 2
image[:, (image.shape[1] - 1) // 2] = 2

plt.imshow(image)
plt.show()
