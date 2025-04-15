# SPDX-FileCopyrightText: 2024-present Olivier Delrée <olivierdelree@protonmail.com>
#
# SPDX-License-Identifier: MIT

import logging
import os
from typing import Optional

import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets

from histalign.backend.ccf.paths import get_annotation_path
from histalign.backend.io import clear_directory, RESOURCES_ROOT
from histalign.backend.maths import apply_rotation, compute_centre, compute_origin
from histalign.backend.models import Orientation, ProjectSettings
from histalign.backend.workspace import AnnotationVolume, VolumeLoaderThread, Workspace
from histalign.frontend.common_widgets import (
    BasicApplicationWindow,
    BasicMenuBar,
    DynamicThemeIcon,
    MouseTrackingFilter,
    ShortcutAwareToolButton,
)
from histalign.frontend.dialogs import (
    AtlasProgressDialog,
    ConfirmDeleteDialog,
    InvalidProjectFileDialog,
    NewProjectDialog,
    SaveProjectConfirmationDialog,
)
from histalign.frontend.registration.alignment import (
    AlignmentWidget,
    LandmarkRegistrationWindow,
)
from histalign.frontend.registration.alpha import AlphaWidget
from histalign.frontend.registration.helpers import get_dummy_title_bar
from histalign.frontend.registration.settings import SettingsWidget
from histalign.frontend.registration.thumbnails import ThumbnailsWidget


class RegistrationMenuBar(BasicMenuBar):
    action_groups: dict[str, list[QtWidgets.QMenu | QtGui.QAction]]

    new_action: QtGui.QAction
    save_action: QtGui.QAction
    open_directory_action: QtGui.QAction

    new_requested: QtCore.Signal = QtCore.Signal()
    save_requested: QtCore.Signal = QtCore.Signal()
    open_directory_requested: QtCore.Signal = QtCore.Signal()

    lut_change_requested: QtCore.Signal = QtCore.Signal(str)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        #
        project_required_group = []

        self.action_groups = {"project_required": project_required_group}

        #
        new_action = QtGui.QAction("&New", self.file_menu)

        new_action.setStatusTip("Create a new project")
        new_action.setShortcut(QtGui.QKeySequence("Ctrl+n"))
        new_action.setShortcutContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        new_action.triggered.connect(self.new_requested.emit)

        self.new_action = new_action

        #
        save_action = QtGui.QAction("&Save", self.file_menu)

        save_action.setStatusTip("Save the current project")
        save_action.setShortcut(QtGui.QKeySequence("Ctrl+Shift+s"))
        save_action.setShortcutContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        save_action.triggered.connect(self.save_requested.emit)
        save_action.setEnabled(False)
        project_required_group.append(save_action)

        self.save_action = save_action

        #
        open_directory_action = QtGui.QAction("Open &image directory", self)

        open_directory_action.setStatusTip("Open an image directory for alignment")
        open_directory_action.setShortcut(QtGui.QKeySequence("Ctrl+Shift+o"))
        open_directory_action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        open_directory_action.triggered.connect(self.open_directory_requested.emit)
        open_directory_action.setEnabled(False)
        project_required_group.append(open_directory_action)

        self.open_directory_action = open_directory_action

        #
        self.file_menu.insertAction(self.open_action, new_action)
        self.file_menu.insertAction(self.close_action, save_action)
        self.file_menu.insertSeparator(self.close_action)
        # A bit flaky since separators are in added order which might not match visual
        self.file_menu.insertAction(
            [
                action
                for action in self.file_menu.findChildren(QtGui.QAction)
                if action.isSeparator()
            ][0],
            open_directory_action,
        )

        #
        lut_menu = self.addMenu("&LUT")

        lut_menu.setEnabled(False)
        self.action_groups["project_required"].append(lut_menu)

        #
        lut_group = QtGui.QActionGroup(lut_menu)

        lut_group.triggered.connect(
            lambda action: self.lut_change_requested.emit(action.toolTip().lower())
        )

        grey_lut_action = QtGui.QAction("Gr&ey")
        grey_lut_action.setCheckable(True)
        grey_lut_action.setChecked(True)
        lut_group.addAction(grey_lut_action)
        lut_menu.addAction(grey_lut_action)
        red_lut_action = QtGui.QAction("&Red")
        red_lut_action.setCheckable(True)
        lut_group.addAction(red_lut_action)
        lut_menu.addAction(red_lut_action)
        green_lut_action = QtGui.QAction("&Green")
        green_lut_action.setCheckable(True)
        lut_group.addAction(green_lut_action)
        lut_menu.addAction(green_lut_action)
        blue_lut_action = QtGui.QAction("&Blue")
        blue_lut_action.setCheckable(True)
        lut_group.addAction(blue_lut_action)
        lut_menu.addAction(blue_lut_action)
        cyan_lut_action = QtGui.QAction("&Cyan")
        cyan_lut_action.setCheckable(True)
        lut_group.addAction(cyan_lut_action)
        lut_menu.addAction(cyan_lut_action)
        magenta_lut_action = QtGui.QAction("&Magenta")
        magenta_lut_action.setCheckable(True)
        lut_group.addAction(magenta_lut_action)
        lut_menu.addAction(magenta_lut_action)
        yellow_lut_action = QtGui.QAction("&Yellow")
        yellow_lut_action.setCheckable(True)
        lut_group.addAction(yellow_lut_action)
        lut_menu.addAction(yellow_lut_action)

    def opened_project(self) -> None:
        for action in self.action_groups["project_required"]:
            action.setEnabled(True)


class RegistrationToolBar(QtWidgets.QToolBar):
    save_button: ShortcutAwareToolButton
    load_button: ShortcutAwareToolButton
    delete_button: ShortcutAwareToolButton
    reset_histology_button: ShortcutAwareToolButton
    reset_volume_button: ShortcutAwareToolButton
    apply_auto_threshold_button: ShortcutAwareToolButton
    background_threshold_spin_box: QtWidgets.QSpinBox
    landmark_registration_button: ShortcutAwareToolButton

    save_requested: QtCore.Signal = QtCore.Signal()
    load_requested: QtCore.Signal = QtCore.Signal()
    delete_requested: QtCore.Signal = QtCore.Signal()
    reset_histology_requested: QtCore.Signal = QtCore.Signal()
    reset_volume_requested: QtCore.Signal = QtCore.Signal()
    apply_auto_threshold_requested: QtCore.Signal = QtCore.Signal()
    background_threshold_changed: QtCore.Signal = QtCore.Signal(int)
    landmark_registration_requested: QtCore.Signal = QtCore.Signal()

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        #
        save_button = ShortcutAwareToolButton()

        save_button.setShortcut(QtGui.QKeySequence("Ctrl+s"))
        save_button.setToolTip("Save alignment for the current image. ")
        save_button.setStatusTip("Save alignment for the current image.")
        save_button.setIcon(
            DynamicThemeIcon(RESOURCES_ROOT / "icons" / "file-black-icon.png")
        )

        save_button.clicked.connect(self.save_requested.emit)

        self.save_button = save_button

        #
        load_button = ShortcutAwareToolButton()

        load_button.setToolTip("Load the saved alignment for the current image.")
        load_button.setStatusTip("Load the saved alignment for the current image.")
        load_button.setIcon(
            DynamicThemeIcon(RESOURCES_ROOT / "icons" / "upload-arrow-icon.png")
        )

        load_button.clicked.connect(self.load_requested.emit)
        load_button.setShortcut(QtGui.QKeySequence("Ctrl+l"))

        self.load_button = load_button

        #
        delete_button = ShortcutAwareToolButton()

        delete_button.setToolTip("Delete the saved alignment for the current image.")
        delete_button.setStatusTip("Delete the saved alignment for the current image.")
        delete_button.setIcon(
            DynamicThemeIcon(RESOURCES_ROOT / "icons" / "recycle-bin-icon.png")
        )

        delete_button.clicked.connect(self.delete_requested.emit)

        self.delete_button = delete_button

        #
        reset_histology_button = ShortcutAwareToolButton()

        reset_histology_button.setToolTip("Reset the image alignment settings.")
        reset_histology_button.setStatusTip("Reset the image alignment settings.")
        reset_histology_button.setIcon(
            DynamicThemeIcon(RESOURCES_ROOT / "icons" / "forward-restore-icon.png")
        )

        reset_histology_button.clicked.connect(self.reset_histology_requested.emit)
        reset_histology_button.setShortcut(QtGui.QKeySequence("Ctrl+r"))

        self.reset_histology_button = reset_histology_button

        #
        reset_volume_button = ShortcutAwareToolButton()

        reset_volume_button.setToolTip("Reset the atlas alignment settings.")
        reset_volume_button.setStatusTip("Reset the atlas alignment settings.")
        reset_volume_button.setIcon(
            DynamicThemeIcon(RESOURCES_ROOT / "icons" / "forward-restore-icon.png")
        )

        reset_volume_button.clicked.connect(self.reset_volume_requested.emit)
        reset_volume_button.setShortcut(QtGui.QKeySequence("Ctrl+Shift+r"))

        self.reset_volume_button = reset_volume_button

        #
        apply_auto_threshold_button = ShortcutAwareToolButton()

        apply_auto_threshold_button.setToolTip(
            "Apply a pass of ImageJ's brightness/contrast auto-thresholding algorithm."
        )
        apply_auto_threshold_button.setStatusTip(
            "Apply a pass of ImageJ's brightness/contrast auto-thresholding algorithm."
        )
        apply_auto_threshold_button.setIcon(
            DynamicThemeIcon(RESOURCES_ROOT / "icons" / "background-icon.png")
        )

        apply_auto_threshold_button.clicked.connect(
            self.apply_auto_threshold_requested.emit
        )
        apply_auto_threshold_button.setShortcut(QtGui.QKeySequence("Ctrl+Shift+c"))

        self.apply_auto_threshold_button = apply_auto_threshold_button

        #
        background_spin_box_icon = QtWidgets.QToolButton()

        background_spin_box_icon.setIcon(
            DynamicThemeIcon(RESOURCES_ROOT / "icons" / "color-contrast-icon.png")
        )
        background_spin_box_icon.setStyleSheet(
            """
            QToolButton:hover {
                border: none;
            }
            """
        )

        #
        background_spin_box = QtWidgets.QSpinBox()

        background_spin_box.setToolTip("Set the background transparency threshold.")
        background_spin_box.setStatusTip("Set the background transparency threshold.")
        background_spin_box.setMinimum(0)
        background_spin_box.setMaximum(255)
        background_spin_box.setValue(0)
        background_spin_box.valueChanged.connect(
            lambda x: self.background_threshold_changed.emit(x)
        )

        self.background_threshold_spin_box = background_spin_box

        #
        landmark_registration_button = ShortcutAwareToolButton()

        landmark_registration_button.setToolTip(
            "Start the landmark registration process."
        )
        landmark_registration_button.setStatusTip(
            "Start the landmark registration process."
        )
        landmark_registration_button.setIcon(
            DynamicThemeIcon(RESOURCES_ROOT / "icons" / "interactivity-icon.png")
        )

        landmark_registration_button.clicked.connect(
            self.landmark_registration_requested.emit
        )

        self.landmark_registration_button = landmark_registration_button

        #
        self.addWidget(save_button)
        self.addWidget(load_button)
        self.addWidget(delete_button)
        self.addSeparator()
        self.addWidget(reset_histology_button)
        self.addWidget(reset_volume_button)
        self.addSeparator()
        self.addWidget(apply_auto_threshold_button)
        self.addSeparator()
        self.addWidget(background_spin_box_icon)
        self.addWidget(background_spin_box)
        self.addSeparator()
        self.addWidget(landmark_registration_button)

        #
        self.setAllowedAreas(QtCore.Qt.ToolBarArea.TopToolBarArea)
        self.setMovable(False)


class RegistrationMainWindow(BasicApplicationWindow):
    workspace: Optional[Workspace] = None
    workspace_loaded: bool = False
    workspace_dirtied: bool = False

    annotation_volume: Optional[AnnotationVolume] = None

    toolbar: RegistrationToolBar
    alignment_widget: AlignmentWidget
    thumbnails_widget: ThumbnailsWidget
    alpha_widget: AlphaWidget
    settings_widget: SettingsWidget

    project_closed: QtCore.Signal = QtCore.Signal()

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        #
        super().__init__(parent)

        self.logger = logging.getLogger(
            f"{self.__module__}.{self.__class__.__qualname__}"
        )

        #
        alignment_widget = AlignmentWidget()

        alignment_widget.view.installEventFilter(
            MouseTrackingFilter(
                tracking_callback=self.locate_mouse,
                leaving_callback=self.clear_status,
                watched_type=QtWidgets.QGraphicsView,
                parent=alignment_widget.view,
            )
        )

        self.alignment_widget = alignment_widget

        #
        thumbnails_widget = ThumbnailsWidget()

        thumbnails_widget.thumbnail_activated.connect(self.open_image_in_aligner)

        self.thumbnails_widget = thumbnails_widget

        #
        alpha_widget = AlphaWidget()

        alpha_widget.global_alpha_slider.valueChanged.connect(
            alignment_widget.update_global_alpha
        )

        self.alpha_widget = alpha_widget

        #
        settings_widget = SettingsWidget()

        settings_widget.volume_settings_widget.setEnabled(False)
        settings_widget.volume_settings_widget.values_changed.connect(
            alignment_widget.update_volume_pixmap
        )
        settings_widget.histology_settings_widget.setEnabled(False)
        settings_widget.histology_settings_widget.values_changed.connect(
            alignment_widget.update_histology_pixmap
        )

        alignment_widget.translation_changed.connect(
            settings_widget.histology_settings_widget.handle_outside_translation
        )
        alignment_widget.rotation_changed.connect(
            settings_widget.histology_settings_widget.handle_outside_rotation
        )
        alignment_widget.zoom_changed.connect(
            settings_widget.histology_settings_widget.handle_outside_zoom
        )

        self.settings_widget = settings_widget

        #
        layout = QtWidgets.QHBoxLayout()

        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        layout.addWidget(thumbnails_widget, stretch=1)
        layout.addWidget(alignment_widget, stretch=3)
        layout.addWidget(alpha_widget)
        layout.addWidget(settings_widget, stretch=1)

        #
        central_widget = QtWidgets.QWidget()

        central_widget.setLayout(layout)
        central_widget.statusBar = self.statusBar

        self.setCentralWidget(central_widget)

        #
        toolbar = RegistrationToolBar()

        toolbar.save_button.setEnabled(False)
        toolbar.load_button.setEnabled(False)
        toolbar.delete_button.setEnabled(False)
        toolbar.reset_histology_button.setEnabled(False)
        toolbar.reset_volume_button.setEnabled(False)
        toolbar.apply_auto_threshold_button.setEnabled(False)
        toolbar.landmark_registration_button.setEnabled(False)

        toolbar.save_requested.connect(lambda: toolbar.load_button.setEnabled(True))
        toolbar.save_requested.connect(lambda: toolbar.delete_button.setEnabled(True))
        toolbar.save_requested.connect(
            lambda: toolbar.apply_auto_threshold_button.setEnabled(True)
        )
        toolbar.save_requested.connect(
            lambda: self.thumbnails_widget.set_thumbnail_completed(
                self.workspace.current_aligner_image_index, True
            )
        )

        toolbar.delete_requested.connect(self.show_confirm_delete_alignment_dialog)

        toolbar.background_threshold_changed.connect(
            alignment_widget.update_background_alpha
        )
        toolbar.reset_histology_requested.connect(
            settings_widget.histology_settings_widget.reset_to_defaults
        )
        toolbar.reset_volume_requested.connect(
            settings_widget.volume_settings_widget.reset_to_defaults
        )
        toolbar.apply_auto_threshold_requested.connect(
            self.alignment_widget.apply_auto_contrast
        )
        toolbar.landmark_registration_requested.connect(
            self.show_landmark_registration_window
        )

        self.addToolBar(toolbar)
        self.toolbar = toolbar

    def set_up_menu_bar(self) -> None:
        menu_bar = RegistrationMenuBar()

        menu_bar.new_requested.connect(self.show_new_project_dialog)
        menu_bar.open_requested.connect(self.show_open_project_dialog)
        menu_bar.save_requested.connect(self.save_project)
        menu_bar.close_requested.connect(self.close_project)
        menu_bar.open_directory_requested.connect(self.show_open_image_directory_dialog)
        menu_bar.exit_requested.connect(self.exit_application)

        menu_bar.lut_change_requested.connect(
            lambda x: self.alignment_widget.update_lut(x)
        )

        self.setMenuBar(menu_bar)

    def propagate_new_workspace(self) -> None:
        self.connect_workspace()
        self.share_workspace_models()

        # Sync states
        self.alignment_widget.prepare_slicer()

        # Block signals for improved responsiveness
        self.settings_widget.volume_settings_widget.blockSignals(True)
        self.settings_widget.histology_settings_widget.blockSignals(True)
        self.settings_widget.reload_settings()
        self.settings_widget.volume_settings_widget.blockSignals(False)
        self.settings_widget.histology_settings_widget.blockSignals(False)

        for index, slice_ in enumerate(self.workspace._histology_slices):
            if not os.path.exists(
                self.workspace.working_directory + os.sep + slice_.hash + ".json"
            ):
                continue

            self.thumbnails_widget.set_thumbnail_completed(index, True)

    def connect_workspace(self) -> None:
        self.thumbnails_widget.connect_workspace(self.workspace)

        toolbar = self.toolbar

        toolbar.save_requested.connect(self.workspace.save_alignment)
        toolbar.save_requested.connect(
            lambda: self.statusBar().showMessage("Alignment saved", 2000)
        )

        toolbar.load_requested.connect(self.workspace.load_alignment)
        toolbar.load_requested.connect(
            lambda: self.statusBar().showMessage("Alignment loaded", 2000)
        )
        toolbar.load_requested.connect(self.share_workspace_models)
        toolbar.load_requested.connect(self.settings_widget.reload_settings)

    def share_workspace_models(self) -> None:
        alignment_settings = self.workspace.alignment_settings
        volume_settings = self.workspace.alignment_settings.volume_settings
        histology_settings = self.workspace.alignment_settings.histology_settings

        self.alignment_widget.alignment_settings = alignment_settings
        self.alignment_widget.volume_settings = volume_settings
        self.alignment_widget.histology_settings = histology_settings

        self.settings_widget.volume_settings_widget.settings = (
            self.workspace.alignment_settings.volume_settings
        )
        self.settings_widget.histology_settings_widget.settings = histology_settings

    def load_atlas(self) -> int:
        # Gather the volumes
        # Sneak the annotation volume in here. It doesn't usually take long but if
        # it turns out to in the future, we can give feedback to the user.
        annotation_volume = AnnotationVolume(
            get_annotation_path(self.workspace.resolution),
            self.workspace.resolution,
            lazy=True,
        )
        self.annotation_volume = annotation_volume
        atlas_volume = self.alignment_widget.volume_slicer.volume

        # Set up the dialog and loader threads
        dialog = AtlasProgressDialog(self)
        annotation_loader_thread = VolumeLoaderThread(annotation_volume)
        atlas_loader_thread = VolumeLoaderThread(atlas_volume)

        dialog.rejected.connect(lambda: self.logger.debug("Cancelling loader threads."))
        dialog.rejected.connect(annotation_loader_thread.requestInterruption)
        dialog.rejected.connect(atlas_loader_thread.requestInterruption)

        atlas_volume.downloaded.connect(
            lambda: dialog.setLabelText("Loading atlas"),
            type=QtCore.Qt.ConnectionType.QueuedConnection,
        )
        atlas_volume.loaded.connect(
            dialog.accept, type=QtCore.Qt.ConnectionType.QueuedConnection
        )
        atlas_volume.loaded.connect(
            self.open_atlas_in_aligner, type=QtCore.Qt.ConnectionType.QueuedConnection
        )

        # Start dialog and threads
        annotation_loader_thread.start()
        atlas_loader_thread.start()

        result = dialog.exec()  # Blocking

        # Ensure we wait for the threads to be destroyed
        annotation_loader_thread.wait()
        atlas_loader_thread.wait()

        return result

    def dirty_workspace(self) -> None:
        if self.workspace_loaded:
            self.workspace_dirtied = True

    def locate_mouse(self) -> None:
        if self.annotation_volume is None:
            return

        widget = self.alignment_widget
        orientation = widget.volume_settings.orientation
        pitch = widget.volume_settings.pitch
        yaw = widget.volume_settings.yaw

        # Get global cursor position
        global_position = QtGui.QCursor.pos()

        # Convert it to a view position
        view_position = widget.view.mapFromGlobal(global_position)

        # Convert it to a scene position
        scene_position = widget.view.mapToScene(view_position)

        # Convert it to a pixmap position
        pixmap_position = widget.volume_pixmap.mapFromScene(scene_position).toTuple()
        # NOTE: there is no need to flip the X coordinate of the pixmap position even
        #       though the image undergoes `np.fliplr` when slicing. That is because
        #       pixmap coordinates increase from left to right which is correct for
        #       volume coordinates.

        # Compute position of pixmap centre
        pixmap_centre_position = widget.volume_pixmap.pixmap().size().toTuple()
        pixmap_centre_position = np.array(pixmap_centre_position) // 2

        # Compute relative cursor pixmap position from centre
        relative_pixmap_position = pixmap_position - pixmap_centre_position
        relative_pixmap_position = relative_pixmap_position  # X x Y not I x J

        # Convert to non-rotated coordinates
        match orientation:
            case Orientation.CORONAL:
                pixmap_coordinates = [
                    0,
                    relative_pixmap_position[1],
                    relative_pixmap_position[0],
                ]
            case Orientation.HORIZONTAL:
                pixmap_coordinates = [
                    relative_pixmap_position[1],
                    0,
                    relative_pixmap_position[0],
                ]
            case Orientation.SAGITTAL:
                pixmap_coordinates = [
                    relative_pixmap_position[0],
                    relative_pixmap_position[1],
                    0,
                ]
            case other:
                raise Exception(f"ASSERT NOT REACHED: {other}")
        pixmap_coordinates = np.array(pixmap_coordinates)

        # Apply rotation
        rotated_coordinates = apply_rotation(pixmap_coordinates, widget.volume_settings)

        # Add to slicing plane origin
        volume_centre = compute_centre(widget.volume_settings.shape)
        volume_origin = compute_origin(volume_centre, widget.volume_settings)

        volume_coordinates = volume_origin + rotated_coordinates
        volume_coordinates = np.array(list(map(int, volume_coordinates)))

        # Get the name of the structure at coordinates
        structure_name = self.annotation_volume.get_name_from_voxel(volume_coordinates)
        structure_string = f" ({structure_name})" if structure_name else ""

        # Convert volume coordinates to CCF coordinates
        ccf_coordinates = volume_coordinates * widget.volume_settings.resolution.value

        # Display output in status bar
        self.statusBar().showMessage(
            f"CCF coordinates of cursor: "
            f"{', '.join(map(str, map(round, map(int, ccf_coordinates))))}"
            f"{structure_string}"
        )

    def clear_status(self) -> None:
        self.statusBar().clearMessage()

    def cancel_project_open(self) -> None:
        self.logger.debug("Cancelling opening of project.")

        # Clear aligner
        self.close_atlas_in_aligner()
        self.close_image_in_aligner()
        self.annotation_volume = None

        # Clear thumbnails
        self.thumbnails_widget.flush_thumbnails()

        # Reset settings
        self.settings_widget.reset_to_defaults(silent=True)

        # Stop the workspace
        self.workspace.stop_thumbnail_generation()
        # Keep a reference to it to avoid killing the thumbnail QThread while it is
        # still alive.
        self._workspace = self.workspace
        self.workspace = None

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.workspace is not None:
            if not self.workspace_dirtied:
                event.accept()
                return

            match SaveProjectConfirmationDialog(self).exec():
                case QtWidgets.QMessageBox.Save:
                    self.save_project()
                    event.accept()
                case QtWidgets.QMessageBox.Discard:
                    event.accept()
                case QtWidgets.QMessageBox.Cancel:
                    event.ignore()

            self.workspace.stop_thumbnail_generation()

    @QtCore.Slot()
    def show_new_project_dialog(self) -> None:
        if self.workspace is not None and self.workspace_dirtied:
            match SaveProjectConfirmationDialog(self).exec():
                case QtWidgets.QMessageBox.Save:
                    self.save_project()
                case QtWidgets.QMessageBox.Cancel:
                    return None

        dialog = NewProjectDialog(self)
        dialog.submitted.connect(self.create_project)
        dialog.exec()

    @QtCore.Slot()
    def show_open_project_dialog(self) -> None:
        if self.workspace is not None and self.workspace_dirtied:
            match SaveProjectConfirmationDialog(self).exec():
                case QtWidgets.QMessageBox.Save:
                    self.save_project()
                case QtWidgets.QMessageBox.Cancel:
                    return

        super().show_open_project_dialog()

    @QtCore.Slot()
    def show_open_image_directory_dialog(self) -> None:
        image_directory = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select an image directory",
            os.getcwd(),
            options=QtWidgets.QFileDialog.Option.DontUseNativeDialog,
        )

        if image_directory != "":
            self.dirty_workspace()
            self.alignment_widget.update_histological_slice(None)
            self.thumbnails_widget.flush_thumbnails()
            self.workspace.parse_image_directory(image_directory)
            self.workspace.start_thumbnail_generation()

    @QtCore.Slot()
    def show_confirm_delete_alignment_dialog(self) -> None:
        dialog = ConfirmDeleteDialog(self)

        if dialog.exec() != QtWidgets.QMessageBox.StandardButton.Ok:
            return

        self.workspace.delete_alignment()
        self.statusBar().showMessage("Deleted alignment", 2000)
        self.thumbnails_widget.set_thumbnail_completed(
            self.workspace.current_aligner_image_index, False
        )

        self.toolbar.load_button.setEnabled(False)
        self.toolbar.delete_button.setEnabled(False)

    @QtCore.Slot()
    def show_landmark_registration_window(self) -> None:
        window = LandmarkRegistrationWindow(self)

        match self.workspace.alignment_settings.volume_settings.orientation:
            case Orientation.CORONAL:
                general_zoom = 2.0
            case Orientation.HORIZONTAL:
                general_zoom = 1.5
            case Orientation.SAGITTAL:
                general_zoom = 1.7
            case _:
                raise Exception("ASSERT NOT REACHED")

        window.update_reference_pixmap(
            self.alignment_widget.volume_pixmap, general_zoom
        )
        window.update_histology_pixmap(self.alignment_widget.histology_pixmap)

        window.resize(
            QtCore.QSize(
                round(self.width() * 0.95),
                round(self.height() * 0.95),
            )
        )
        window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        window.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

        window.applied.connect(
            self.alignment_widget.update_alignment_from_landmark_registration
        )
        window.applied.connect(self.settings_widget.reload_settings)

        window.show()

    @QtCore.Slot()
    def create_project(self, project_settings: ProjectSettings) -> None:
        clear_directory(project_settings.project_path)

        self.alignment_widget.reset_histology()

        self.workspace = Workspace(project_settings)
        self.propagate_new_workspace()

        self.workspace.start_thumbnail_generation()
        if self.load_atlas() == QtWidgets.QDialog.DialogCode.Rejected:
            return self.cancel_project_open()

        self.menuBar().opened_project()

        self.workspace_loaded = True
        self.dirty_workspace()

    @QtCore.Slot()
    def open_project(self, project_file_path: str) -> None:
        self.alignment_widget.reset_histology()

        try:
            self.workspace = Workspace.load(project_file_path)
        except ValueError:
            return InvalidProjectFileDialog(self).open()

        self.propagate_new_workspace()

        self.workspace.start_thumbnail_generation()
        if self.load_atlas() == QtWidgets.QDialog.DialogCode.Rejected:
            return self.cancel_project_open()

        if self.workspace.current_aligner_image_hash is not None:
            self.open_image_in_aligner(
                self.workspace.current_aligner_image_index, force_open=True
            )

        self.menuBar().opened_project()

        self.workspace_loaded = True
        self.workspace_dirtied = False

    @QtCore.Slot()
    def save_project(self) -> None:
        self.workspace.save()
        self.workspace_dirtied = False

    @QtCore.Slot()
    def open_atlas_in_aligner(self) -> None:
        self.logger.debug("Opening atlas.")

        # noinspection PyTypeChecker
        self.workspace.alignment_settings.volume_settings.shape = (
            self.alignment_widget.volume_slicer.volume.shape
        )

        try:
            self.alignment_widget.update_volume_pixmap(rescale=True)
        except ValueError as error:
            self.logger.error("Could not open atlas volume.")
            self.logger.error(error)
            return

        self.toolbar.reset_volume_button.setEnabled(True)

        self.settings_widget.volume_settings_widget.update_offset_spin_box_limits()
        self.settings_widget.volume_settings_widget.reload_settings()
        self.settings_widget.volume_settings_widget.setEnabled(True)

        # Easiest way to trigger scale ratio calculations
        self.alignment_widget.resizeEvent(
            QtGui.QResizeEvent(
                self.alignment_widget.size(), self.alignment_widget.size()
            )
        )

    @QtCore.Slot()
    def close_atlas_in_aligner(self) -> None:
        self.logger.debug("Closing atlas.")

        self.alignment_widget.reset_volume()

        self.toolbar.reset_volume_button.setEnabled(False)

        self.settings_widget.volume_settings_widget.reset_to_defaults(silent=True)
        self.settings_widget.volume_settings_widget.setEnabled(False)

    @QtCore.Slot()
    def open_image_in_aligner(self, index: int, force_open: bool = False) -> None:
        if (
            self.workspace is None
            or self.workspace.current_aligner_image_index == index
            and not force_open
        ):
            return

        self.dirty_workspace()

        old_index = self.workspace.current_aligner_image_index

        image = self.workspace.get_image(index)
        if image is None:
            if len(self.workspace._histology_slices) > 0:
                self.logger.error(
                    f"Failed retrieving image at index {index}, index out of range."
                )
            return

        self.alignment_widget.update_histological_slice(image)
        self.alignment_widget.update_background_alpha(
            self.toolbar.background_threshold_spin_box.value()
        )
        self.alignment_widget.update_global_alpha(
            self.alpha_widget.global_alpha_slider.value()
        )
        self.toolbar.save_button.setEnabled(True)

        self.toolbar.load_button.setEnabled(
            os.path.exists(self.workspace.build_alignment_path())
        )
        self.toolbar.delete_button.setEnabled(
            os.path.exists(self.workspace.build_alignment_path())
        )

        self.toolbar.reset_histology_button.setEnabled(True)
        self.settings_widget.histology_settings_widget.setEnabled(True)
        self.toolbar.apply_auto_threshold_button.setEnabled(True)
        self.toolbar.landmark_registration_button.setEnabled(True)

        if old_index is not None:
            self.thumbnails_widget.make_thumbnail_at_active(old_index)
        if old_index != index:
            self.thumbnails_widget.make_thumbnail_at_active(index)

    @QtCore.Slot()
    def close_image_in_aligner(self) -> None:
        self.alignment_widget.reset_histology()

        self.toolbar.save_button.setEnabled(False)
        self.toolbar.delete_button.setEnabled(False)
        self.toolbar.reset_histology_button.setEnabled(False)
        self.toolbar.apply_auto_threshold_button.setEnabled(False)
        self.toolbar.landmark_registration_button.setEnabled(False)
        self.settings_widget.histology_settings_widget.setEnabled(False)
