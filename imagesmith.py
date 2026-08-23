import sys
import os
import base64
import io
from PIL import Image, ImageOps, ImageEnhance
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QScrollArea, QMessageBox, QGroupBox, QLineEdit, QSlider, QSizePolicy
)
from PyQt6.QtGui import QImage, QPixmap, QMouseEvent, QDragEnterEvent, QDropEvent, QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer

class InteractiveLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAcceptDrops(True)
        self.parent_window = parent
        self.mode = None

        self.crop_rect = QRect()
        self.resizing_edge = None
        self.drag_start_pos = QPoint()
        self.initial_rect = QRect()
        self.setMinimumSize(100, 100)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls(): event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls: self.parent_window.load_image_from_path(urls[0].toLocalFile())

    def get_handle_at(self, pos: QPoint):
        if self.crop_rect.isNull(): return None
        r, margin = self.crop_rect, 12
        left, right = abs(pos.x() - r.left()) <= margin, abs(pos.x() - r.right()) <= margin
        top, bottom = abs(pos.y() - r.top()) <= margin, abs(pos.y() - r.bottom()) <= margin

        in_x, in_y = r.left() - margin <= pos.x() <= r.right() + margin, r.top() - margin <= pos.y() <= r.bottom() + margin

        if left and top: return "top_left"
        if right and top: return "top_right"
        if left and bottom: return "bottom_left"
        if right and bottom: return "bottom_right"
        if top and in_x: return "top"
        if bottom and in_x: return "bottom"
        if left and in_y: return "left"
        if right and in_y: return "right"
        if r.contains(pos): return "move"
        return "new"

    def mousePressEvent(self, event: QMouseEvent):
        if self.mode == 'crop' and event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self.resizing_edge = self.get_handle_at(pos)
            self.drag_start_pos = pos
            self.initial_rect = self.crop_rect
            if self.resizing_edge == "new" or self.crop_rect.isNull():
                self.resizing_edge = "new"
                self.crop_rect = QRect(pos, pos)
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.mode == 'crop' and self.resizing_edge:
            pos = event.pos()
            dx, dy = pos.x() - self.drag_start_pos.x(), pos.y() - self.drag_start_pos.y()
            r = QRect(self.initial_rect)
            if self.resizing_edge == "new": self.crop_rect = QRect(self.drag_start_pos, pos).normalized()
            elif self.resizing_edge == "move": r.translate(dx, dy); self.crop_rect = r
            else:
                if "left" in self.resizing_edge: r.setLeft(r.left() + dx)
                if "right" in self.resizing_edge: r.setRight(r.right() + dx)
                if "top" in self.resizing_edge: r.setTop(r.top() + dy)
                if "bottom" in self.resizing_edge: r.setBottom(r.bottom() + dy)
                self.crop_rect = r.normalized()
            self.parent_window.check_pending_changes()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.mode == 'crop' and event.button() == Qt.MouseButton.LeftButton:
            self.resizing_edge = None
            self.crop_rect = self.crop_rect.normalized()
            self.parent_window.check_pending_changes()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.mode == 'crop' and not self.crop_rect.isNull():
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            painter.fillRect(self.crop_rect, QColor(0, 0, 0, 0))

            color = QColor(231, 76, 60)
            painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.DashLine))
            painter.drawRect(self.crop_rect)
            painter.setPen(QPen(color, 2, Qt.PenStyle.SolidLine))
            painter.drawRect(self.crop_rect)

            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            r = self.crop_rect
            handles = [QPoint(r.left(), r.top()), QPoint(r.center().x(), r.top()), QPoint(r.right(), r.top()),
                       QPoint(r.left(), r.center().y()), QPoint(r.right(), r.center().y()), QPoint(r.left(), r.bottom()),
                       QPoint(r.center().x(), r.bottom()), QPoint(r.right(), r.bottom())]
            for pt in handles: painter.drawRect(pt.x()-4, pt.y()-4, 8, 8)


class BasicImageFixer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image_path = None
        self.pil_image = None
        self.preview_image = None
        self.history = []

        self.pulse_value = 43
        self.pulse_direction = 1
        self.pulse_timer = QTimer(self)
        self.pulse_timer.setInterval(50)
        self.pulse_timer.timeout.connect(self.update_pulse_effect)

    def initUI(self):
        self.setWindowTitle("ImageSmith")
        self.resize(750, 750)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget#TopHeaderBar {
                background-color: #1b365d;
                border-radius: 4px;
            }
            QLabel#HeaderLabel {
                background-color: transparent;
                color: #ffffff;
                font-weight: bold;
                font-size: 13px;
                padding: 6px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        top_bar_widget = QWidget()
        top_bar_widget.setObjectName("TopHeaderBar")
        top_bar_layout = QVBoxLayout(top_bar_widget)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.lbl_info = QLabel("Dimensions: No image loaded")
        self.lbl_info.setObjectName("HeaderLabel")
        self.lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_bar_layout.addWidget(self.lbl_info)

        layout.addWidget(top_bar_widget)

        file_layout = QHBoxLayout()
        self.btn_open = QPushButton("Open Image")
        self.btn_open.clicked.connect(self.open_image_dialog)
        file_layout.addWidget(self.btn_open)

        self.btn_undo = QPushButton("⟲ Undo")
        self.btn_undo.clicked.connect(self.undo_action)
        self.btn_undo.setEnabled(False)
        file_layout.addWidget(self.btn_undo)

        self.btn_save = QPushButton("Save Copy (Source Folder)")
        self.btn_save.clicked.connect(self.save_image)
        self.btn_save.setEnabled(False)
        file_layout.addWidget(self.btn_save)

        layout.addLayout(file_layout)

        self.image_label = InteractiveLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("Drag & Drop")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setStyleSheet("QScrollArea { background-color: #2b2b2b; border: none; }")
        layout.addWidget(self.scroll_area)

        self.resize_group = QGroupBox("📐 Resize Image")
        self.resize_group.setStyleSheet("QGroupBox { color: #3498db; font-weight: bold; border: 1px solid #3498db; border-radius: 5px; margin-top: 5px; padding-top: 15px; }")
        resize_layout = QHBoxLayout()

        resize_layout.addWidget(QLabel("Width:"))
        self.input_w = QLineEdit()
        self.input_w.setPlaceholderText("Width")
        self.input_w.textChanged.connect(self.check_pending_changes)
        resize_layout.addWidget(self.input_w)

        resize_layout.addWidget(QLabel("Height:"))
        self.input_h = QLineEdit()
        self.input_h.setPlaceholderText("Height")
        self.input_h.textChanged.connect(self.check_pending_changes)
        resize_layout.addWidget(self.input_h)

        self.resize_group.setLayout(resize_layout)
        self.resize_group.hide()
        layout.addWidget(self.resize_group)

        self.slider_group = QGroupBox("⬒ Tilt / Perspective Controls")
        self.slider_group.setStyleSheet("QGroupBox { color: #f39c12; font-weight: bold; border: 1px solid #f39c12; border-radius: 5px; margin-top: 5px; padding-top: 15px; }")
        slider_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Horizontal Tilt (Left/Right):"))
        self.slider_h = QSlider(Qt.Orientation.Horizontal)
        self.slider_h.setRange(-40, 40)
        self.slider_h.setValue(0)
        self.slider_h.setTracking(True)
        self.slider_h.valueChanged.connect(self.on_slider_changed)
        h_layout.addWidget(self.slider_h)
        slider_layout.addLayout(h_layout)

        v_layout = QHBoxLayout()
        v_layout.addWidget(QLabel("Vertical Tilt (Top/Bottom):"))
        self.slider_v = QSlider(Qt.Orientation.Horizontal)
        self.slider_v.setRange(-40, 40)
        self.slider_v.setValue(0)
        self.slider_v.setTracking(True)
        self.slider_v.valueChanged.connect(self.on_slider_changed)
        v_layout.addWidget(self.slider_v)
        slider_layout.addLayout(v_layout)

        self.slider_group.setLayout(slider_layout)
        self.slider_group.hide()
        layout.addWidget(self.slider_group)

        self.pad_color_group = QGroupBox("🎨 Pad Square Border Color")
        self.pad_color_group.setStyleSheet("QGroupBox { color: #f1c40f; font-weight: bold; border: 1px solid #f1c40f; border-radius: 5px; margin-top: 5px; padding-top: 15px; }")
        pad_color_layout = QHBoxLayout()

        self.pad_colors = ["Black", "White", "Gray", "Red", "Green", "Blue", "Orange", "Yellow", "Purple"]
        self.pad_color_buttons = {}

        for color_name in self.pad_colors:
            btn = QPushButton(color_name)
            btn.clicked.connect(lambda checked, c=color_name: self.apply_pad_square(c))
            pad_color_layout.addWidget(btn)
            self.pad_color_buttons[color_name] = btn

        self.pad_color_group.setLayout(pad_color_layout)
        self.pad_color_group.hide()
        layout.addWidget(self.pad_color_group)

        tools_layout = QHBoxLayout()

        self.btn_enhance = QPushButton("✨ Enhance")
        self.btn_enhance.clicked.connect(self.auto_enhance)
        tools_layout.addWidget(self.btn_enhance)

        self.btn_crop = QPushButton("✂ Crop")
        self.btn_crop.setCheckable(True)
        self.btn_crop.clicked.connect(lambda: self.set_mode('crop'))
        tools_layout.addWidget(self.btn_crop)

        self.btn_resize_toggle = QPushButton("📐 Resize")
        self.btn_resize_toggle.setCheckable(True)
        self.btn_resize_toggle.clicked.connect(lambda: self.set_mode('resize'))
        tools_layout.addWidget(self.btn_resize_toggle)

        self.btn_tilt = QPushButton("⬒ Tilt")
        self.btn_tilt.setCheckable(True)
        self.btn_tilt.clicked.connect(lambda: self.set_mode('perspective'))
        tools_layout.addWidget(self.btn_tilt)

        self.btn_apply = QPushButton("✓ Apply Action")
        self.btn_apply.clicked.connect(self.apply_action)
        self.btn_apply.setEnabled(False)
        tools_layout.addWidget(self.btn_apply)

        self.btn_rotate = QPushButton("Rotate 90°")
        self.btn_rotate.clicked.connect(self.rotate_image)
        tools_layout.addWidget(self.btn_rotate)

        self.btn_square = QPushButton("Pad Square")
        self.btn_square.setCheckable(True)
        self.btn_square.clicked.connect(self.toggle_pad_mode)
        tools_layout.addWidget(self.btn_square)

        for btn in [self.btn_enhance, self.btn_crop, self.btn_resize_toggle, self.btn_tilt, self.btn_rotate, self.btn_square]:
            btn.setEnabled(False)

        layout.addLayout(tools_layout)

    def save_state(self):
        if self.pil_image:
            self.history.append(self.pil_image.copy())
            self.btn_undo.setEnabled(True)

    def open_image_dialog(self):
        dialog = QFileDialog(self, "Open Image", os.path.expanduser("~"))
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.ico *.svg)")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)

        if dialog.exec():
            files = dialog.selectedFiles()
            if files:
                self.load_image_from_path(files[0])

    def load_image_from_path(self, file_path):
        self.image_path = file_path

        if file_path.lower().endswith('.svg'):
            try:
                import cairosvg
                png_bytes = cairosvg.svg2png(url=file_path, output_width=1024)
                raw_img = Image.open(io.BytesIO(png_bytes))
                self.pil_image = raw_img.convert("RGBA")
            except Exception as e:
                try:
                    self.pil_image = Image.open(file_path).convert("RGBA")
                except Exception as inner_e:
                    QMessageBox.warning(self, "SVG Load Error", f"Could not render SVG file:\n{inner_e}")
                    return
        else:
            raw_img = Image.open(file_path)
            self.pil_image = raw_img.convert("RGBA")

        self.preview_image = self.pil_image.copy()
        self.history.clear()
        self.update_display()
        self.enable_tools(True)

    def update_display(self, img_to_show=None):
        target_img = img_to_show if img_to_show else self.pil_image
        if not target_img:
            return

        w, h = target_img.size
        filename = os.path.basename(self.image_path) if self.image_path else "Unsaved"
        self.lbl_info.setText(f"File: {filename}  |  Dimensions: {w} × {h} pixels")

        im = target_img.convert("RGBA")
        data = im.tobytes("raw", "RGBA")
        qim = QImage(data, im.width, im.height, QImage.Format.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qim)

        max_w, max_h = 620, 320
        if pixmap.width() > max_w or pixmap.height() > max_h:
            pixmap = pixmap.scaled(max_w, max_h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.image_label.setPixmap(pixmap)
        self.image_label.resize(pixmap.size())
        if not img_to_show:
            self.image_label.crop_rect = QRect()
        self.check_pending_changes()

    def enable_tools(self, state):
        self.btn_save.setEnabled(state)
        self.btn_undo.setEnabled(len(self.history) > 0)
        self.btn_enhance.setEnabled(state)
        self.btn_crop.setEnabled(state)
        self.btn_resize_toggle.setEnabled(state)
        self.btn_tilt.setEnabled(state)
        self.btn_rotate.setEnabled(state)
        self.btn_square.setEnabled(state)

    def undo_action(self):
        if self.history:
            self.pil_image = self.history.pop()
            self.preview_image = self.pil_image.copy()
            self.update_display()
            if not self.history:
                self.btn_undo.setEnabled(False)
        self.check_pending_changes()

    def set_mode(self, mode):
        self.pad_color_group.hide()
        self.btn_square.setChecked(False)

        if self.image_label.mode == mode:
            self.image_label.mode = None
            self.image_label.crop_rect = QRect()
            self.resize_group.hide()
            self.slider_group.hide()
            self.preview_image = self.pil_image.copy()
            self.update_display()
        else:
            self.image_label.mode = mode
            if mode == 'crop':
                self.resize_group.hide()
                self.slider_group.hide()
                if self.pil_image:
                    lbl_size = self.image_label.size()
                    w, h = lbl_size.width(), lbl_size.height()
                    self.image_label.crop_rect = QRect(int(w * 0.1), int(h * 0.1), int(w * 0.8), int(h * 0.8))
            elif mode == 'resize':
                self.resize_group.show()
                self.slider_group.hide()
                if self.pil_image:
                    self.input_w.setText(str(self.pil_image.width))
                    self.input_h.setText(str(self.pil_image.height))
            elif mode == 'perspective':
                self.resize_group.hide()
                self.slider_group.show()
                self.slider_h.blockSignals(True)
                self.slider_v.blockSignals(True)
                self.slider_h.setValue(0)
                self.slider_v.setValue(0)
                self.slider_h.blockSignals(False)
                self.slider_v.blockSignals(False)
                self.preview_image = self.pil_image.copy()

        self.btn_crop.setChecked(self.image_label.mode == 'crop')
        self.btn_resize_toggle.setChecked(self.image_label.mode == 'resize')
        self.btn_tilt.setChecked(self.image_label.mode == 'perspective')
        self.image_label.update()
        self.check_pending_changes()

    def toggle_pad_mode(self):
        self.resize_group.hide()
        self.slider_group.hide()
        self.image_label.mode = None
        self.btn_crop.setChecked(False)
        self.btn_resize_toggle.setChecked(False)
        self.btn_tilt.setChecked(False)
        self.image_label.update()

        if self.pad_color_group.isVisible():
            self.pad_color_group.hide()
            self.btn_square.setChecked(False)
        else:
            self.pad_color_group.show()
            self.btn_square.setChecked(True)

    def check_pending_changes(self):
        has_pending = False
        mode = self.image_label.mode

        if mode == 'crop':
            rect = self.image_label.crop_rect
            if rect and not rect.isNull() and (rect.width() > 5 or rect.height() > 5):
                has_pending = True
        elif mode == 'perspective':
            if self.slider_h.value() != 0 or self.slider_v.value() != 0:
                has_pending = True
        elif mode == 'resize':
            try:
                w = int(self.input_w.text())
                h = int(self.input_h.text())
                if self.pil_image and (w != self.pil_image.width or h != self.pil_image.height):
                    has_pending = True
            except ValueError:
                pass

        self.btn_apply.setEnabled(has_pending)

        if has_pending:
            if not self.pulse_timer.isActive():
                self.pulse_timer.start()
        else:
            self.pulse_timer.stop()
            self.btn_apply.setStyleSheet("")

    def update_pulse_effect(self):
        self.pulse_value += self.pulse_direction * 4
        if self.pulse_value >= 110:
            self.pulse_value = 110
            self.pulse_direction = -1
        elif self.pulse_value <= 35:
            self.pulse_value = 35
            self.pulse_direction = 1

        self.btn_apply.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb(27, {self.pulse_value}, 46);
                color: white;
                border: 1px solid #2ea44f;
                font-weight: bold;
                border-radius: 4px;
                padding: 5px;
            }}
        """)

    def on_slider_changed(self):
        self.check_pending_changes()
        if self.image_label.mode != 'perspective' or self.pil_image is None:
            return

        h_val = self.slider_h.value()
        v_val = self.slider_v.value()

        if h_val == 0 and v_val == 0:
            self.preview_image = self.pil_image.copy()
            self.update_display(self.preview_image)
            return

        src = self.pil_image
        w, h = src.size

        pad = int(max(w, h) * 0.10)
        canvas_w = w + pad * 2
        canvas_h = h + pad * 2

        canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        canvas.paste(src, (pad, pad), src)

        left = float(pad)
        top = float(pad)
        right = float(pad + w)
        bottom = float(pad + h)

        max_shift_x = w * 0.10
        max_shift_y = h * 0.10

        shift_x = (h_val / 40.0) * max_shift_x
        shift_y = (v_val / 40.0) * max_shift_y

        top_left = (left + shift_x, top + shift_y)
        bottom_left = (left - shift_x, bottom + shift_y)
        bottom_right = (right + shift_x, bottom - shift_y)
        top_right = (right - shift_x, top - shift_y)

        quad = (
            top_left[0], top_left[1],
            bottom_left[0], bottom_left[1],
            bottom_right[0], bottom_right[1],
            top_right[0], top_right[1]
        )

        try:
            transformed = canvas.transform(
                (canvas_w, canvas_h),
                Image.Transform.QUAD,
                quad,
                resample=Image.Resampling.BICUBIC
            )
            self.preview_image = transformed.crop((pad, pad, pad + w, pad + h))
            self.update_display(self.preview_image)
        except Exception as e:
            print(f"Transform error: {e}")

    def apply_action(self):
        if not self.pil_image:
            return

        self.save_state()
        mode = self.image_label.mode

        if mode == 'crop':
            rect = self.image_label.crop_rect
            if not rect or rect.isNull() or rect.width() < 5 or rect.height() < 5:
                QMessageBox.warning(self, "Crop Error", "Please adjust the crop box first.")
                self.history.pop()
                return

            label_size = self.image_label.size()
            scale_x = self.pil_image.width / label_size.width()
            scale_y = self.pil_image.height / label_size.height()

            left = max(0, int(rect.x() * scale_x))
            top = max(0, int(rect.y() * scale_y))
            right = min(self.pil_image.width, int((rect.x() + rect.width()) * scale_x))
            lower = min(self.pil_image.height, int((rect.y() + rect.height()) * scale_y))

            if right > left and lower > top:
                self.pil_image = self.pil_image.crop((left, top, right, lower))

        elif mode == 'perspective':
            if self.preview_image:
                self.pil_image = self.preview_image.copy()

        elif mode == 'resize':
            try:
                new_w = int(self.input_w.text())
                new_h = int(self.input_h.text())
                if new_w <= 0 or new_h <= 0:
                    raise ValueError("Dimensions must be greater than zero.")
                self.pil_image = self.pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
            except ValueError as e:
                QMessageBox.warning(self, "Resize Error", f"Please enter valid numeric dimensions:\n{e}")
                self.history.pop()
                return

        self.image_label.mode = None
        self.btn_crop.setChecked(False)
        self.btn_resize_toggle.setChecked(False)
        self.btn_tilt.setChecked(False)
        self.resize_group.hide()
        self.slider_group.hide()
        self.preview_image = self.pil_image.copy()
        self.update_display()

    def auto_enhance(self):
        self.save_state()
        working_image = self.pil_image.convert("RGB")
        enhanced = ImageOps.autocontrast(working_image, cutoff=2)
        enhanced = ImageEnhance.Color(enhanced).enhance(1.2)
        enhanced = ImageEnhance.Contrast(enhanced).enhance(1.1)
        enhanced = ImageEnhance.Sharpness(enhanced).enhance(1.3)
        self.pil_image = enhanced.convert("RGBA")
        self.preview_image = self.pil_image.copy()
        self.update_display()

    def rotate_image(self):
        self.save_state()
        self.pil_image = self.pil_image.rotate(-90, expand=True)
        self.preview_image = self.pil_image.copy()
        self.update_display()

    def apply_pad_square(self, color_name):
        if not self.pil_image:
            return

        self.save_state()
        w, h = self.pil_image.size
        max_dim = max(w, h)

        color_map = {
            "Black": (0, 0, 0),
            "White": (255, 255, 255),
            "Gray": (128, 128, 128),
            "Red": (231, 76, 60),
            "Green": (46, 204, 113),
            "Blue": (52, 152, 219),
            "Orange": (230, 126, 34),
            "Yellow": (241, 196, 15),
            "Purple": (155, 89, 182)
        }

        bg_rgb = color_map.get(color_name, (0, 0, 0))

        new_img = Image.new("RGB", (max_dim, max_dim), bg_rgb)
        offset = ((max_dim - w) // 2, (max_dim - h) // 2)

        if self.pil_image.mode == 'RGBA':
            new_img.paste(self.pil_image, offset, self.pil_image)
        else:
            new_img.paste(self.pil_image, offset)

        self.pil_image = new_img.convert("RGBA")
        self.preview_image = self.pil_image.copy()

        self.pad_color_group.hide()
        self.btn_square.setChecked(False)
        self.update_display()

    def save_image(self):
        if not self.pil_image or not self.image_path:
            return

        source_dir = os.path.dirname(self.image_path)
        file_name = os.path.basename(self.image_path)
        name_part, file_ext = os.path.splitext(file_name)

        if "_imagesmith" in name_part:
            name_part = name_part.split("_imagesmith")[0]

        default_ext = file_ext if file_ext else ".png"

        counter = 0
        while True:
            if counter == 0:
                default_save_name = os.path.join(source_dir, f"{name_part}{default_ext}")
            else:
                default_save_name = os.path.join(source_dir, f"{name_part}_{counter}{default_ext}")

            if not os.path.exists(default_save_name):
                break
            counter += 1

        filter_str = (
            "PNG Image (*.png);; "
            "JPEG Image (*.jpg *.jpeg);; "
            "WebP Image (*.webp);; "
            "Bitmap Image (*.bmp);; "
            "TIFF Image (*.tiff);; "
            "Vector SVG (*.svg)"
        )

        save_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Save Copy in Source Folder", default_save_name, filter_str
        )

        if not save_path:
            return

        if save_path.lower().endswith('.svg') or "SVG" in selected_filter:
            if not save_path.lower().endswith('.svg'):
                save_path += '.svg'
            try:
                buffered = io.BytesIO()
                self.pil_image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                width, height = self.pil_image.size
                svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <image width="{width}" height="{height}" href="data:image/png;base64,{img_str}"/>
</svg>'''
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(svg_content)
                QMessageBox.information(self, "Saved Copy", f"Exported vector-wrapped copy to:\n{save_path}")
            except Exception as e:
                QMessageBox.warning(self, "Export Error", f"SVG creation failed:\n{e}")
            return

        ext_map = {"PNG": ".png", "JPEG": ".jpg", "WebP": ".webp", "Bitmap": ".bmp", "TIFF": ".tiff"}
        target_ext = None
        for key, extension in ext_map.items():
            if key in selected_filter:
                target_ext = extension
                break

        if target_ext and not save_path.lower().endswith(tuple(ext_map.values())):
            save_path += target_ext

        img_to_save = self.pil_image
        if save_path.lower().endswith(('.jpg', '.jpeg')) and img_to_save.mode == 'RGBA':
            rgb_img = Image.new("RGB", img_to_save.size, (255, 255, 255))
            rgb_img.paste(img_to_save, mask=img_to_save.split()[3])
            img_to_save = rgb_img

        img_to_save.save(save_path)
        QMessageBox.information(self, "Saved Copy", f"Created independent copy at:\n{save_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BasicImageFixer()
    ex.show()
    sys.exit(app.exec())
