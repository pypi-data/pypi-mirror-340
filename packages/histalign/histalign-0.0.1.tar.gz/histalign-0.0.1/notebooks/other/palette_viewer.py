# SPDX-FileCopyrightText: 2024-present Olivier Delrée <olivierdelree@protonmail.com>
#
# SPDX-License-Identifier: MIT

import signal
import sys
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

from histalign.frontend.themes import DARK_THEME, LIGHT_THEME


signal.signal(signal.SIGINT, signal.SIG_DFL)


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        #
        layout = QtWidgets.QFormLayout()

        for role in QtGui.QPalette.ColorRole:
            label = QtWidgets.QLabel()

            palette = label.palette()
            palette.setColor(QtGui.QPalette.ColorRole.Window, palette.color(role))
            label.setPalette(palette)

            label.setAutoFillBackground(True)

            layout.addRow(str(role), label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    # app.setStyleSheet("* { border: 1px solid blue; }")

    app.setPalette(LIGHT_THEME)

    window = MyWidget()
    window.resize(600, 600)
    window.show()

    sys.exit(app.exec())
