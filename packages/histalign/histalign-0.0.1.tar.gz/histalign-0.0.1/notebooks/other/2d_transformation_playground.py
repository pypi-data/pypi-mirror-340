# SPDX-FileCopyrightText: 2024-present Olivier Delrée <olivierdelree@protonmail.com>
#
# SPDX-License-Identifier: MIT

import math
import sys
from typing import Optional

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
import skimage.transform as transform

# Create an empty image
shape = (200, 200)
array = np.zeros(shape, dtype=np.uint8)

# Add features
# Add a line one-quarter from the left
array[:, shape[1] // 4] = 255
# Add a bent line one-quarter from the right
array[
    np.linspace(0, shape[0] // 2, shape[0] // 2).astype(int),
    np.round(np.linspace(shape[1] // 2, shape[1] * 3 // 4, shape[0] // 2)).astype(int),
] = 255
array[shape[0] // 2 :, shape[1] * 3 // 4] = 255


def get_sk_transform_from_parameters(
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0,
    shear: tuple[float, float] = (0.0, 0.0),
    translation: tuple[float, float] = (0.0, 0.0),
) -> transform.AffineTransform:
    # `transform.AffineTransform` uses shearing angles instead of coordinate shift.
    # The angles are also clockwise hence the correction factor.
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
    sk_transform = transform.AffineTransform(
        scale=scale,
        rotation=math.radians(rotation),
        shear=shear_angles,
        translation=translation,
    )

    return sk_transform


def convert_sk_transform_to_q_transform(
    transformation: transform.AffineTransform,
) -> QtGui.QTransform:
    q_transform = QtGui.QTransform()
    q_transform.setMatrix(*transformation.params.T.flatten().tolist())

    return q_transform


class Widget(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

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

        for i in range(-1000, 1001, 50):
            scene.addLine(i, -1000, i, 1000)
            scene.addLine(-1000, i, 1000, i)

        for i in range(-1000, 1001, 50):
            text = scene.addText(str(int(i / 50)))
            text.setTransform(QtGui.QTransform().translate(i, 0))
            text = scene.addText(str(int(i / 50)))
            text.setTransform(QtGui.QTransform().translate(0, i))

        self.scene = scene

        #
        view = QtWidgets.QGraphicsView(scene)

        view.setSceneRect(
            QtCore.QRect(-shape[0], -shape[1], 3 * shape[0], 3 * shape[1])
        )

        self.view = view

        #
        pixmap_item = scene.addPixmap(pixmap)

        pixmap_item.setOffset(-shape[0] / 2, -shape[1] / 2)

        self.pixmap_item = pixmap_item

        #
        position_button = QtWidgets.QPushButton("info")

        position_button.clicked.connect(
            lambda: print(
                f"Top left: {self.pixmap_item.sceneBoundingRect().topLeft()}\n"
                f"Bottom right: {self.pixmap_item.sceneBoundingRect().bottomRight()}\n"
                f"Centre: {self.pixmap_item.sceneBoundingRect().center()}\n"
                f"Matrix:\n"
                f" [{self.pixmap_item.transform().m11():<5.3f}, {self.pixmap_item.transform().m21():<5.3f}, {self.pixmap_item.transform().m31():<5.3f}]\n",
                f"[{self.pixmap_item.transform().m12():<5.3f}, {self.pixmap_item.transform().m22():<5.3f}, {self.pixmap_item.transform().m32():<5.3f}]\n",
                f"[{self.pixmap_item.transform().m13():<5.3f}, {self.pixmap_item.transform().m23():<5.3f}, {self.pixmap_item.transform().m33():<5.3f}]",
            )
        )

        self.position_button = position_button

        #
        translate_positive_button = QtWidgets.QPushButton("translate+")

        translate_positive_button.clicked.connect(
            lambda: setattr(self, "x_translate", self.x_translate + 50)
        )
        translate_positive_button.clicked.connect(
            lambda: setattr(self, "y_translate", self.y_translate + 50)
        )
        translate_positive_button.clicked.connect(self.update_transform)

        self.translate_positive_button = translate_positive_button

        #
        translate_negative_button = QtWidgets.QPushButton("translate-")

        translate_negative_button.clicked.connect(
            lambda: setattr(self, "x_translate", self.x_translate - 50)
        )
        translate_negative_button.clicked.connect(
            lambda: setattr(self, "y_translate", self.y_translate - 50)
        )
        translate_negative_button.clicked.connect(self.update_transform)

        self.translate_negative_button = translate_negative_button

        #
        scale_positive_button = QtWidgets.QPushButton("scale+")

        scale_positive_button.clicked.connect(
            lambda: setattr(self, "x_scale", self.x_scale + 0.1)
        )
        scale_positive_button.clicked.connect(
            lambda: setattr(self, "y_scale", self.y_scale + 0.1)
        )
        scale_positive_button.clicked.connect(self.update_transform)

        self.scale_positive_button = scale_positive_button

        #
        scale_negative_button = QtWidgets.QPushButton("scale-")

        scale_negative_button.clicked.connect(
            lambda: setattr(self, "x_scale", self.x_scale - 0.1)
        )
        scale_negative_button.clicked.connect(
            lambda: setattr(self, "y_scale", self.y_scale - 0.1)
        )
        scale_negative_button.clicked.connect(self.update_transform)

        self.scale_negative_button = scale_negative_button

        #
        shear_positive_button = QtWidgets.QPushButton("shear+")

        shear_positive_button.clicked.connect(
            lambda: setattr(self, "x_shear", self.x_shear + 0.1)
        )
        shear_positive_button.clicked.connect(
            lambda: setattr(self, "y_shear", self.y_shear + 0.1)
        )
        shear_positive_button.clicked.connect(self.update_transform)

        self.shear_positive_button = shear_positive_button

        #
        shear_negative_button = QtWidgets.QPushButton("shear-")

        shear_negative_button.clicked.connect(
            lambda: setattr(self, "x_shear", self.x_shear - 0.1)
        )
        shear_negative_button.clicked.connect(
            lambda: setattr(self, "y_shear", self.y_shear - 0.1)
        )
        shear_negative_button.clicked.connect(self.update_transform)

        self.shear_negative_button = shear_negative_button

        #
        rotate_positive_button = QtWidgets.QPushButton("rotate+")

        rotate_positive_button.clicked.connect(
            lambda: setattr(self, "rotate", self.rotate + 30)
        )
        rotate_positive_button.clicked.connect(self.update_transform)

        self.rotate_positive_button = rotate_positive_button

        #
        rotate_negative_button = QtWidgets.QPushButton("rotate-")

        rotate_negative_button.clicked.connect(
            lambda: setattr(self, "rotate", self.rotate - 30)
        )
        rotate_negative_button.clicked.connect(self.update_transform)

        self.rotate_negative_button = rotate_negative_button

        #
        clear_button = QtWidgets.QPushButton("Clear")

        clear_button.clicked.connect(self.clear_transform)

        self.clear_button = clear_button

        #
        save_button = QtWidgets.QPushButton("Save")

        save_button.clicked.connect(lambda: view.grab().save("out.png"))

        self.save_button = save_button

        #
        layout = QtWidgets.QGridLayout()

        layout.addWidget(view, 0, 0, -1, 1)
        layout.addWidget(position_button, 0, 1)
        layout.addWidget(translate_positive_button, 1, 1)
        layout.addWidget(translate_negative_button, 1, 2)
        layout.addWidget(rotate_positive_button, 2, 1)
        layout.addWidget(rotate_negative_button, 2, 2)
        layout.addWidget(scale_positive_button, 3, 1)
        layout.addWidget(scale_negative_button, 3, 2)
        layout.addWidget(shear_positive_button, 4, 1)
        layout.addWidget(shear_negative_button, 4, 2)
        layout.addWidget(clear_button, 5, 1)
        layout.addWidget(save_button, 6, 1)

        self.setLayout(layout)

        #
        self.clear_transform()

    def update_transform(self) -> None:
        sk_transform = get_sk_transform_from_parameters(
            scale=(self.x_scale, self.y_scale),
            shear=(self.x_shear, self.y_shear),
            translation=(self.x_translate, self.y_translate),
            rotation=self.rotate,
        )
        q_transform = convert_sk_transform_to_q_transform(sk_transform)

        self.pixmap_item.setTransform(q_transform)

    def clear_transform(self) -> None:
        self.x_translate = 0
        self.y_translate = 0
        self.x_scale = 1.0
        self.y_scale = 1.0
        self.x_shear = 0.0
        self.y_shear = 0.0
        self.rotate = 0

        self.pixmap_item.resetTransform()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    # app.setStyleSheet("* { border: 1px solid blue; }")

    window = Widget()
    window.resize(1000, 1000)
    window.show()

    sys.exit(app.exec())
