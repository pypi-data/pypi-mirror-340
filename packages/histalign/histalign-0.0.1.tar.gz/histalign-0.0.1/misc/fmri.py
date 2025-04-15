# SPDX-FileCopyrightText: 2025-present Olivier Delrée <olivierdelree@protonmail.com>
#
# SPDX-License-Identifier: MIT

from pathlib import Path
from typing import Optional

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
import vedo

from histalign.backend.ccf.paths import get_atlas_path
from histalign.backend.io import load_volume, RESOURCES_ROOT
from histalign.backend.models import Resolution
from histalign.backend.preprocessing import normalise_array
from histalign.frontend.common_widgets import (
    BinaryAlphaPixmap,
    CheckableLabel,
    HoverButton,
    ZoomAndPanView,
)
from histalign.frontend.pyside_helpers import lua_aware_shift, np_to_qpixmap


class CheckableLabel(QtWidgets.QWidget):
    """A label widget with an attached check box.

    By clicking the label or the check box, the check box state is changed.

    Signals:
        state_changed: bool
    """

    label: CutOffLabel
    check_box: QtWidgets.QCheckBox

    state_changed: QtCore.Signal = QtCore.Signal(bool)

    def __init__(
        self,
        text: str,
        check_box_position: Literal["left", "right"] = "left",
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        """A label widget with an attached check box.

        Args:
            text (str): Text to set the label to.
            check_box_position (Literal["left", "right"], optional):
                Position of the check box relative to the label.
            parent (QtWidgets.QWidget, optional): Parent of this widget.
        """

        super().__init__(parent)

        #
        check_box = QtWidgets.QCheckBox()

        check_box.checkStateChanged.connect(
            lambda state: self.state_changed.emit(state == QtCore.Qt.CheckState.Checked)
        )

        self.check_box = check_box

        #
        label = CutOffLabel(text)

        self.label = label

        #
        layout = QtWidgets.QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        if check_box_position == "left":
            layout.addWidget(check_box)
            layout.addWidget(label, stretch=1)
        elif check_box_position == "right":
            layout.addWidget(label, stretch=1)
            layout.addWidget(check_box)
        else:
            raise ValueError(f"Unknown check box position: {check_box_position}.")

        self.setLayout(layout)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.rect().contains(event.position().toPoint()):
            self.check_box.setChecked(not self.check_box.isChecked())
        else:
            super().mouseReleaseEvent(event)


class SummaryFMRIWidget(QtWidgets.QWidget):
    def __init__(
        self,
        text: str = "Brain Viewer",
        file_path: str | Path = "",
        volume: Optional[np.ndarray | vedo.Volume] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)

        #
        header = SummaryFMRIHeader(text)

        self.header = header

        #
        coronal_scene = QtWidgets.QGraphicsScene()

        coronal_scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.black))

        self.coronal_scene = coronal_scene

        coronal_view = ZoomAndPanView(coronal_scene)

        coronal_view.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        coronal_view.set_zoom_modifier(QtCore.Qt.KeyboardModifier.ControlModifier)

        self.coronal_view = coronal_view

        #
        horizontal_scene = QtWidgets.QGraphicsScene()

        horizontal_scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.black))

        self.horizontal_scene = horizontal_scene

        horizontal_view = ZoomAndPanView(horizontal_scene)

        horizontal_view.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        horizontal_view.set_zoom_modifier(QtCore.Qt.KeyboardModifier.ControlModifier)

        self.horizontal_view = horizontal_view

        #
        sagittal_scene = QtWidgets.QGraphicsScene()

        sagittal_scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.black))

        self.sagittal_scene = sagittal_scene

        sagittal_view = ZoomAndPanView(sagittal_scene)

        sagittal_view.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        sagittal_view.set_zoom_modifier(QtCore.Qt.KeyboardModifier.ControlModifier)

        self.sagittal_view = sagittal_view

        #
        layout = QtWidgets.QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(header)
        layout.addWidget(coronal_view)
        layout.addWidget(horizontal_view)
        layout.addWidget(sagittal_view)

        self.setLayout(layout)

        #
        if volume is not None:
            if isinstance(volume, vedo.Volume):
                volume = volume.tonumpy()
        elif file_path:
            volume = load_volume(file_path, return_raw_array=True)
        else:
            raise ValueError(
                "Could not load volume as both 'volume' and 'file_path' are missing."
            )

        self.update_views(volume)

    def compute_view_height_from_total_height(self, height: int) -> int:
        height -= self.header.height()
        height /= 3

        return int(height)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        x = self.contentsRect().x()
        y = self.header.rect().bottom()
        width = self.contentsRect().width()
        height = self.compute_view_height_from_total_height(
            self.contentsRect().height()
        )

        self.header.setFixedWidth(width)

        self.coronal_view.setGeometry(QtCore.QRect(x, y, width, height))
        self.coronal_view.setFixedSize(width, height)

        y += height + self.layout().spacing()
        self.horizontal_view.setGeometry(QtCore.QRect(x, y, width, height))
        self.horizontal_view.setFixedSize(width, height)

        y += height + self.layout().spacing()
        self.sagittal_view.setGeometry(QtCore.QRect(x, y, width, height))
        self.sagittal_view.setFixedSize(width, height)

    def sizeHint(self) -> QtCore.QSize:
        spacing = self.layout().spacing()

        header_width = self.header.sizeHint().width()
        header_height = self.header.sizeHint().height()

        height = header_height + 3 * header_width + 3 * spacing
        height += self.contentsMargins().top() + self.contentsMargins().bottom()

        return QtCore.QSize(header_width, height)

    def update_views(self, volume: np.ndarray) -> None:
        # Coronal
        coronal_image = volume[volume.shape[0] // 2]
        self._update_view(self.coronal_view, coronal_image)

        # Horizontal
        horizontal_image = volume[:, volume.shape[1] // 2]
        self._update_view(self.horizontal_view, horizontal_image)

        # Sagittal
        sagittal_image = volume[..., volume.shape[2] // 2]
        sagittal_image = sagittal_image.T
        self._update_view(self.sagittal_view, sagittal_image)

    @staticmethod
    def _update_view(view: ZoomAndPanView, image: np.ndarray) -> None:
        image = normalise_array(image)

        pixmap = np_to_qpixmap(image)
        item = view.scene().addPixmap(pixmap)

        view.set_focus_rect(item.sceneBoundingRect())


class SummaryFMRIHeader(QtWidgets.QWidget):
    def __init__(self, title: str, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        #
        palette = self.palette()

        palette.setColor(
            QtGui.QPalette.ColorRole.Button,
            lua_aware_shift(palette.window().color(), 20),
        )
        palette.setColor(
            QtGui.QPalette.ColorRole.Window,
            lua_aware_shift(palette.window().color(), 20),
        )

        self.setPalette(palette)

        self.setAutoFillBackground(True)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Maximum,
        )

        #
        checkable_label = CheckableLabel(title)

        self.checkable_label = checkable_label

        #
        information_button = HoverButton(icon_path="resources/icons/info-icon.png")

        information_button.setPalette(palette)

        self.information_button = information_button

        #
        layout = QtWidgets.QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(checkable_label)
        layout.addWidget(information_button)

        self.setLayout(layout)

        #
        self.setContentsMargins(3, 2, 3, 2)
