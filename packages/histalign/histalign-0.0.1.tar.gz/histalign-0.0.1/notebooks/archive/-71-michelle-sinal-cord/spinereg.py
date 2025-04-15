# SPDX-FileCopyrightText: 2025-present Olivier Delrée <olivierdelree@protonmail.com>
#
# SPDX-License-Identifier: MIT

import signal
import sys
from typing import Optional

import h5py
import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from collections.abc import Sequence
import math

import numpy as np
from PySide6 import QtGui
from scipy.spatial.transform import Rotation
from skimage.transform import AffineTransform
import vedo

from histalign.backend.models import (
    Orientation,
    VolumeSettings,
)
from histalign.backend.models.errors import InvalidOrientationError
from histalign.frontend.common_widgets import DraggableSpinBox, DraggableDoubleSpinBox

signal.signal(signal.SIGINT, signal.SIG_DFL)


class TitleFrame(QtWidgets.QFrame):
    """A frame which holds its title on the frame.

    A rough representation looks like so:
     -- Title -----------
    |                    |
    |                    |
     -- -----------------

    Attributes:
        title (str): Title of the frame
        bold (bool): Whether to render the title bold.
        italic (bool): Whether to render the title in italics.
    """

    def __init__(
        self,
        title: str = "",
        bold: bool = False,
        italic: bool = False,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)

        #
        # Add space padding to avoid clipping on Windows
        if title:
            title = " " + title + " "
        self.title = title
        self.bold = bold
        self.italic = italic

        #
        self.adjust_margins()
        self.setFrameStyle(QtWidgets.QFrame.Shape.Box | QtWidgets.QFrame.Shadow.Plain)

    def adjust_font(self, font: QtGui.QFont) -> None:
        """Adjusts the provided font with own settings.

        The font is modified in-place to use the `bold` and `italic` settings of the
        current object.

        Args:
            font (QtGui.QFont): Font to adjust.
        """
        font.setBold(self.bold)
        font.setItalic(self.italic)

    def adjust_margins(self) -> None:
        """Adjusts the margins to fit the title on the frame."""
        current_font = self.font()

        margin_font = QtGui.QFont(current_font)
        self.adjust_font(margin_font)
        margin_font.setBold(True)

        metrics = QtGui.QFontMetrics(margin_font)
        margin = metrics.boundingRect(self.title).height() - metrics.xHeight()
        # Janky adjustment, seems to work with most "normal" fonts. See `paintEvent`.
        if "win" in sys.platform:
            margin -= self.fontMetrics().xHeight()
        self.setContentsMargins(margin, margin, margin, margin)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Handles paint events.

        The event is handled by painting the frame, erasing the title rect, then drawing
        the title text.

        Args:
            event (QtGui.QPaintEvent): Event to handle.
        """
        super().paintEvent(event)

        painter = QtGui.QPainter(self)

        font = painter.font()
        self.adjust_font(font)
        painter.setFont(font)

        text_option = QtGui.QTextOption(QtCore.Qt.AlignmentFlag.AlignCenter)
        text_option.setWrapMode(QtGui.QTextOption.NoWrap)

        text_rect = (
            painter.fontMetrics().boundingRect(self.title, text_option).toRectF()
        )
        text_rect.moveBottomLeft(self.frameRect().topLeft())
        text_rect.translate(10, painter.fontMetrics().xHeight())
        # Janky adjustment, seems to work with most "normal" fonts I've tested to ensure
        # the text aligns with the frame vertically.
        if "win" in sys.platform:
            text_rect.translate(0, painter.fontMetrics().xHeight())

        erase_rect = QtCore.QRectF(text_rect)
        erase_rect.adjust(-5, 0, 5, 0)
        painter.eraseRect(erase_rect)

        painter.drawText(text_rect, self.title, text_option)


class ButtonControlsWidget(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        #
        open_image_button = QtWidgets.QPushButton("Open image")
        save_registration_button = QtWidgets.QPushButton("Save")
        load_registration_button = QtWidgets.QPushButton("Load")
        reset_registration_button = QtWidgets.QPushButton("Reset")

        #
        layout = QtWidgets.QHBoxLayout()

        layout.addWidget(open_image_button)
        layout.addWidget(save_registration_button)
        layout.addWidget(load_registration_button)
        layout.addWidget(reset_registration_button)

        self.setLayout(layout)


class AffineControlsWidget(QtWidgets.QWidget):
    rotation_changed: QtCore.Signal = QtCore.Signal(float)
    x_translation_changed: QtCore.Signal = QtCore.Signal(int)
    y_translation_changed: QtCore.Signal = QtCore.Signal(int)
    x_scale_changed: QtCore.Signal = QtCore.Signal(float)
    y_scale_changed: QtCore.Signal = QtCore.Signal(float)
    x_shear_changed: QtCore.Signal = QtCore.Signal(float)
    y_shear_changed: QtCore.Signal = QtCore.Signal(float)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        #
        rotation_spin_box = DraggableDoubleSpinBox()
        rotation_spin_box.valueChanged.connect(self.rotation_changed)
        rotation_layout = QtWidgets.QHBoxLayout()
        rotation_layout.addWidget(rotation_spin_box)
        rotation_frame = TitleFrame("Rotation")
        rotation_frame.setLayout(rotation_layout)

        x_translation_spin_box = DraggableSpinBox()
        x_translation_spin_box.valueChanged.connect(self.x_translation_changed)
        x_translation_layout = QtWidgets.QHBoxLayout()
        x_translation_layout.addWidget(x_translation_spin_box)
        x_translation_frame = TitleFrame("X translation")
        x_translation_frame.setLayout(x_translation_layout)

        y_translation_spin_box = DraggableSpinBox()
        y_translation_spin_box.valueChanged.connect(self.y_translation_changed)
        y_translation_layout = QtWidgets.QHBoxLayout()
        y_translation_layout.addWidget(y_translation_spin_box)
        y_translation_frame = TitleFrame("Y translation")
        y_translation_frame.setLayout(y_translation_layout)

        x_scale_spin_box = DraggableDoubleSpinBox()
        x_scale_spin_box.valueChanged.connect(self.x_scale_changed)
        x_scale_layout = QtWidgets.QHBoxLayout()
        x_scale_layout.addWidget(x_scale_spin_box)
        x_scale_frame = TitleFrame("X scaling")
        x_scale_frame.setLayout(x_scale_layout)

        y_scale_spin_box = DraggableDoubleSpinBox()
        y_scale_spin_box.valueChanged.connect(self.y_scale_changed)
        y_scale_layout = QtWidgets.QHBoxLayout()
        y_scale_layout.addWidget(y_scale_spin_box)
        y_scale_frame = TitleFrame("Y scaling")
        y_scale_frame.setLayout(y_scale_layout)

        x_shear_spin_box = DraggableDoubleSpinBox()
        x_shear_spin_box.valueChanged.connect(self.x_shear_changed)
        x_shear_layout = QtWidgets.QHBoxLayout()
        x_shear_layout.addWidget(x_shear_spin_box)
        x_shear_frame = TitleFrame("X shear")
        x_shear_frame.setLayout(x_shear_layout)

        y_shear_spin_box = DraggableDoubleSpinBox()
        y_shear_spin_box.valueChanged.connect(self.y_shear_changed)
        y_shear_layout = QtWidgets.QHBoxLayout()
        y_shear_layout.addWidget(y_shear_spin_box)
        y_shear_frame = TitleFrame("Y shear")
        y_shear_frame.setLayout(y_shear_layout)

        #
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(rotation_frame)
        layout.addWidget(x_translation_frame)
        layout.addWidget(y_translation_frame)
        layout.addWidget(x_scale_frame)
        layout.addWidget(y_scale_frame)
        layout.addWidget(x_shear_frame)
        layout.addWidget(y_shear_frame)

        layout.addStretch(1)

        self.setLayout(layout)


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        #
        scene = QtWidgets.QGraphicsScene(self)

        self.scene = scene

        #
        view = QtWidgets.QGraphicsView(scene)

        self.view = view

        self.load_reference()

        #
        buttons_controls_widget = ButtonControlsWidget()

        #
        affine_controls_widget = AffineControlsWidget()

        #
        layout = QtWidgets.QGridLayout()

        layout.addWidget(view, 0, 0)

        layout.addWidget(buttons_controls_widget, 1, 0)

        layout.addWidget(affine_controls_widget, 0, 1, -1, 1)

        self.setLayout(layout)

    def load_reference(self) -> None:
        path = "/mnt/c/Users/ediun/Downloads/spinal_cord_contour_c6.h5"

        with h5py.File(path) as handle:
            array = handle["data"][:]

        image = QtGui.QImage(
            array.tobytes(),
            array.shape[1],
            array.shape[0],
            array.shape[1] * 4,
            QtGui.QImage.Format.Format_ARGB32,
        )

        pixmap = QtGui.QPixmap.fromImage(image)
        # pixmap = QtGui.QPixmap(array.shape[1], array.shape[0])
        # pixmap.fill(QtCore.Qt.GlobalColor.red)
        #
        # contour_pixmap = QtGui.QPixmap.fromImage(image)
        #
        # painter = QtGui.QPainter(pixmap)
        # painter.setCompositionMode(
        #     QtGui.QPainter.CompositionMode.CompositionMode_SourceOver
        # )
        # painter.setBrush(
        #     QtGui.QBrush(QtWidgets.QApplication.instance().palette().text())
        # )
        #
        # painter.drawPixmap(QtCore.QPoint(0, 0), contour_pixmap)
        #
        # painter.end()

        pixmap_item = self.scene.addPixmap(pixmap)

        # scaling = max(
        #     self.view.height() / pixmap_item.sceneBoundingRect().height(),
        #     self.view.width() / pixmap_item.sceneBoundingRect().width(),
        # )
        # self.view.scale(scaling, scaling)


def convert_sk_transform_to_q_transform(
    transformation: AffineTransform,
) -> QtGui.QTransform:
    return QtGui.QTransform(*transformation.params.T.flatten().tolist())


def convert_q_transform_to_sk_transform(
    transformation: QtGui.QTransform,
) -> AffineTransform:
    return AffineTransform(
        matrix=get_transformation_matrix_from_q_transform(transformation)
    )


def get_transformation_matrix_from_q_transform(
    transformation: QtGui.QTransform,
    invert: bool = False,
) -> np.ndarray:
    if invert:
        transformation, success = transformation.inverted()
        if not success:
            raise ValueError("Could not invert the affine matrix.")

    # Note that the matrix indices seem to follow an XY notation instead of a classic
    # IJ matrix notation.
    return np.array(
        [
            [transformation.m11(), transformation.m21(), transformation.m31()],
            [transformation.m12(), transformation.m22(), transformation.m32()],
            [transformation.m13(), transformation.m23(), transformation.m33()],
        ]
    )


def get_sk_transform_from_parameters(
    scale: tuple[float, float] = (1.0, 1.0),
    shear: tuple[float, float] = (0.0, 0.0),
    rotation: float = 0.0,
    translation: tuple[float, float] = (0.0, 0.0),
    extra_translation: tuple[float, float] = (0.0, 0.0),
    undo_extra: bool = False,
) -> AffineTransform:
    """Builds a 2D `AffineTransform` from the given parameters.

    This is equivalent to creating an `AffineTransform` from the result of this matrix
    multiplication:
        T @ R @ Sh @ Sc @ Te
    where:
        T is a 3x3 affine transform matrix from `translation`,
        R is a 3x3 affine transform matrix from `rotation`,
        Sc is a 3x3 affine transform matrix from `shear`,
        Sh is a 3x3 affine transform matrix from `scale`,
        Te is a 3x3 affine transform matrix from `extra_translation`.

    Note that unlike `AffineTransform`s `shear` parameter, the `shear` here should
    be a coordinate shift rather than an angle.

    Args:
        scale (tuple[float, float], optional): X and Y scaling factors.
        shear (tuple[float, float], optional):
            X and Y shearing factors. This is a shift in coordinates and not an angle.
        rotation (float, optional): Clockwise rotation in degrees.
        translation (tuple[float, float], optional): X and Y translation factors.
        extra_translation (tuple[float, float], optional):
            Extra translation to apply before all of the other transformations. This
            allows translating the coordinate system before applying the affine
            transform.
        undo_extra (bool, optional):
            Whether to undo the extra translation to return the coordinate system to
            normal.


    Returns:
        AffineTransform: The 2D affine transform whose matrix is obtained from the given
                         parameters.
    """
    # `AffineTransform` uses shearing angles instead of coordinate shift. We therefore
    # compute the equivalent angles on the trigonometric circle. Since the shearing is
    # clockwise, the angle also needs to be inverted for positive shearing.
    x_shear_correction = -1 if shear[0] > 0 else 1
    y_shear_correction = -1 if shear[1] > 0 else 1

    shear_angles = tuple(
        (
            math.acos(
                100 / math.sqrt(100**2 + (shear[0] * 100) ** 2) * x_shear_correction
            ),
            math.acos(
                100 / math.sqrt(100**2 + (shear[1] * 100) ** 2) * y_shear_correction
            ),
        )
    )

    matrix = (
        AffineTransform(
            scale=scale,
            shear=shear_angles,
            rotation=math.radians(rotation),
            translation=translation,
        ).params
        # Apply an extra translation to move the coordinate system
        @ AffineTransform(
            translation=(extra_translation[0], extra_translation[1])
        ).params
    )

    if undo_extra:
        # Move the coordinate system back
        matrix = (
            AffineTransform(
                translation=(
                    -extra_translation[0],
                    -extra_translation[1],
                )
            )
            @ matrix
        )

    return AffineTransform(matrix=matrix)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    # app.setStyleSheet("* { border: 1px solid blue; }")

    window = MyWidget()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
