import matplotlib.pyplot as plt
import numpy as np

from histalign.backend.ccf.paths import get_atlas_path
from histalign.backend.io import load_alignment_settings, load_image, load_volume
from histalign.backend.registration import Registrator
from histalign.backend.workspace import Volume, VolumeSlicer

alignment_path = "/home/ediun/git/histalign/projects/temp/12c22ee785/c1e4a6b68b289dfce5bbd2d54cf24550.json"
alignment_settings = load_alignment_settings(alignment_path)

image = load_image(alignment_settings.histology_path)
image = np.where(image > 3000, image, 0)

atlas: Volume = load_volume(
    get_atlas_path(alignment_settings.volume_settings.resolution)
)
slicer = VolumeSlicer(volume=atlas)
atlas_image = slicer.slice(alignment_settings.volume_settings)

registrator = Registrator(True, True)

reversed_registered = registrator.get_reversed_image(alignment_settings, "atlas", image)

plt.imshow(reversed_registered)
plt.show()

plt.imshow(image)
plt.show()
