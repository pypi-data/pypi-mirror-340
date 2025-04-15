import cv2
import matplotlib.pyplot as plt
import numpy as np

from histalign.backend.ccf.paths import get_atlas_path, get_structure_mask_path
from histalign.backend.io import load_alignment_settings, load_image, load_volume
from histalign.backend.registration import Registrator
from histalign.backend.workspace import Volume, VolumeSlicer

alignment_path = "/home/ediun/git/histalign/projects/temp/3cc119b7ec/9497ca7c45ce883ed494f13e60b22ec5.json"
alignment_settings = load_alignment_settings(alignment_path)

image = load_image(alignment_settings.histology_path)
image = np.where(image > 3000, image, 0)

registrator = Registrator(True, True)

contours = registrator.get_reversed_contours(alignment_settings, "atlas", image)

output_image = np.zeros_like(image)

cv2.drawContours(output_image, contours, -1, (255, 255, 255), 100)

plt.figure()
plt.imshow(np.where(output_image[::10, ::10], 2**16 - 1, image[::10, ::10]))
plt.show()
