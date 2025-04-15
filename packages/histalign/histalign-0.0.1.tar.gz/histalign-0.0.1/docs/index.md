# Getting started

Histalign is an [open-source package](https://github.com/DuguidLab/histalign) that facilitates the registration of two-dimensional histological slices to the [Allen Institute's Brain Atlas](https://portal.brain-map.org/) (CCF). It provides aa graphical user interface (GUI) to permit the user to apply any combination of [affine transformations](https://en.wikipedia.org/wiki/Affine_transformation#Image_transformation) to images obtained through experiments in order to register them to the Allen Institute's Mouse Brain Atlas. In addition, the GUI also provides the ability to build a 3D volume from registered slices as well as interpolating a full volume based on fluorescence.

## Prerequisites
Histalign is meant to work with [HDF5 files](https://www.hdfgroup.org/solutions/hdf5/) (.h5). Future  support might be added for other formats such as TIFF but alignment is limited to HDF5 for the time being.  

In order to carry out alignment, single-channel, two-dimensional images are needed. See [data preparation](tutorials/data-preparation.md) for more details.

## Installing histalign
TODO

## What's next?

For more information on how the GUI works, see the [typical workflow](typical-workflow.md) tutorial which gives you an overview of how data goes through `histalign`.  

For more in-depth guides to each step of the workflow, see the [tutorials](tutorials/index.md)
