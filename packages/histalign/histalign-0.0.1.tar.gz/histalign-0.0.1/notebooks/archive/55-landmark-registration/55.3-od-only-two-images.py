# SPDX-FileCopyrightText: 2024-present Olivier Delrée <olivierdelree@protonmail.com>
#
# SPDX-License-Identifier: MIT

import math
import sys
from typing import Optional

# Fix a typing bug when using `vedo` with python==3.10.12.
# Leaving `typing_extensions.Self` as-is leads to the following error message:
# TypeError: Plain typing.Self is not valid as type argument
# and happens because vedo uses the `Self` annotation in the return type of some
# methods, while it apparently is malformed.
# Avoid being invasive by only patching it when we're the main application.
from typing import TypeVar

import typing_extensions

Self = TypeVar("Self")
typing_extensions.Self = Self

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
import skimage.transform as transform

from histalign.backend.ccf.paths import get_atlas_path
from histalign.backend.io import load_volume
from histalign.backend.models import Resolution

cache = []


def convert_skimage_transform_to_q_transform(
    transformation: transform.AffineTransform,
) -> QtGui.QTransform:
    q_transform = QtGui.QTransform()
    q_transform.setMatrix(*transformation.params.T.flatten().tolist())

    return q_transform


def generate_original_array() -> np.ndarray:
    # array = np.zeros((400,) * 2, dtype=np.uint8)
    # for i in range(array.shape[0]):
    #     array[i, i] = 255
    # array = np.fliplr(array)
    # for i in range(array.shape[0]):
    #     array[i, i] = 255
    # array[:, array.shape[1] // 2] = 255

    array = load_volume(
        get_atlas_path(Resolution.MICRONS_50),
        normalise_dtype=np.uint8,
        return_raw_array=True,
    )
    array = array[100]

    return array


def get_sk_transform_from_parameters(
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
    shear: tuple[float, float] = (0.0, 0.0),
    translation: tuple[float, float] = (0.0, 0.0),
) -> transform.AffineTransform:
    # `transform.AffineTransform` uses shearing angles instead of coordinate shift.
    # The angles are also clockwise, hence the `* -1`.
    shear_angles = tuple(
        (
            math.acos(100 / math.sqrt(100**2 + (shear[0] * 100) ** 2) * -1),
            math.acos(100 / math.sqrt(100**2 + (shear[1] * 100) ** 2) * -1),
        )
    )
    sk_transform = transform.AffineTransform(
        scale=scale,
        rotation=math.radians(rotation),
        shear=shear_angles,
        translation=translation,
    )

    return sk_transform


def get_q_transform_from_parameters(
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
    shear: tuple[float, float] = (0.0, 0.0),
    translation: tuple[float, float] = (0.0, 0.0),
) -> QtGui.QTransform:
    q_transform = (
        QtGui.QTransform()
        .scale(*scale)
        .rotate(rotation)
        .shear(*shear)
        .translate(*translation)
    )

    return q_transform


class EventWatcher(QtCore.QObject):
    def eventFilter(self, watched, event):
        match event.type():
            case QtCore.QEvent.Type.GraphicsSceneMousePress:
                if event.button() == QtCore.Qt.MouseButton.LeftButton:
                    item: QtWidgets.QGraphicsPixmapItem = watched.itemAt(
                        event.scenePos(), QtGui.QTransform()
                    )

                    if item is None:
                        return super().eventFilter(watched, event)

                    pixmap_position = item.mapFromScene(event.scenePos())

                    cache.append(np.array([pixmap_position.y(), pixmap_position.x()]))
                    print(
                        f"IJ coordinate of click: "
                        f"({pixmap_position.y()}, {pixmap_position.x()})"
                    )

                    return True

        return super().eventFilter(watched, event)


class ImageWidget(QtWidgets.QWidget):
    def __init__(
        self,
        array: Optional[np.ndarray] = None,
        transformation: Optional[transform.AffineTransform] = None,
        base_transformation: Optional[QtGui.QTransform] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)

        #
        self.base_transformation = base_transformation

        #
        array = np.zeros((400,) * 2, dtype=np.uint8) if array is None else array

        if isinstance(transformation, transform.AffineTransform):
            array = transform.warp(
                array, transformation, preserve_range=True, clip=True
            ).astype(array.dtype)

        self.array = array

        #
        image = QtGui.QImage(
            array.tobytes(),
            array.shape[1],
            array.shape[0],
            array.shape[1],
            QtGui.QImage.Format.Format_Grayscale8,
        )
        pixmap = QtGui.QPixmap.fromImage(image)

        #
        scene = QtWidgets.QGraphicsScene()

        scene.installEventFilter(watcher)

        self.scene = scene

        #
        view = QtWidgets.QGraphicsView(scene)

        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        view.setSceneRect(QtCore.QRect(0, 0, array.shape[1], array.shape[0]))

        self.view = view

        #
        pixmap_item = scene.addPixmap(pixmap)

        if isinstance(base_transformation, QtGui.QTransform):
            pixmap_item.setTransform(base_transformation)

        self.pixmap_item = pixmap_item

        #
        layout = QtWidgets.QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(view)

        self.setLayout(layout)


class RegistrationWidget(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        #
        original_image_widget = ImageWidget(generate_original_array())

        self.original_image_widget = original_image_widget

        #
        transformed_image_widget = ImageWidget(
            original_image_widget.array,
            get_sk_transform_from_parameters(rotation=20),
            get_q_transform_from_parameters(translation=(10, 50)),
        )

        self.transformed_image_widget = transformed_image_widget

        #
        transform_button = QtWidgets.QPushButton("Transform")

        transform_button.clicked.connect(self.transform)

        self.transform_button = transform_button

        #
        clear_button = QtWidgets.QPushButton("Clear")

        clear_button.clicked.connect(self.clear)

        self.clear_button = clear_button

        #
        layout = QtWidgets.QGridLayout()

        layout.addWidget(original_image_widget, 0, 0)
        layout.addWidget(transformed_image_widget, 0, 1)
        layout.addWidget(transform_button, 1, 0)
        layout.addWidget(clear_button, 1, 1)

        self.setLayout(layout)

    @QtCore.Slot()
    def transform(self) -> None:
        global cache

        if len(cache) % 2 != 0:
            print("NOT EVEN")
            return

        sk_transform = transform.estimate_transform(
            "affine", np.vstack(cache[::2]), np.vstack(cache[1::2])
        )
        q_transform = convert_skimage_transform_to_q_transform(sk_transform.inverse)

        self.transformed_image_widget.pixmap_item.setTransform(
            q_transform.inverted()[0]
        )

    @QtCore.Slot()
    def clear(self) -> None:
        global cache
        cache.clear()

        self.transformed_image_widget.pixmap_item.resetTransform()
        self.transformed_image_widget.pixmap_item.setTransform(
            self.transformed_image_widget.base_transformation
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    # app.setStyleSheet("* { border: 1px solid blue; }")

    watcher = EventWatcher()

    window = RegistrationWidget()
    window.setWindowTitle("Registration GUI")
    # window.resize(600, 600)
    window.show()

    sys.exit(app.exec())
