import os
os.environ['MPLBACKEND'] = 'Qt5Agg'
import sys
import numpy as np
import tifffile as tf
import fabio  # Added for EDF support
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QListWidget, 
                               QSlider, QComboBox, QFileDialog, QInputDialog, 
                               QLineEdit, QMessageBox)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from matplotlib.colors import Normalize, LogNorm, PowerNorm
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class SDFileViewer(QMainWindow):
    def showError(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SD SAXS File Viewer")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #333;
                color: #AAA;
                font-size: 16px;
            }
            QLabel, QSlider {
                font-size: 18px;
            }
            QPushButton {
                background-color: #555;
                font-size: 18px;
                border: 2px solid #888;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #777;
            }
            QListWidget {
                background-color: #222;
                border: 2px solid #000;
                color: #AAA;
            }
            QSlider::groove:horizontal {
                border: 1px solid #888;
                height: 8px;
                background: #555;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #EEE;
                border: 1px solid #888;
                height: 18px;
                width: 18px;
                margin: -10px 0;
            }
        """)
        self.current_image = None
        self.current_dir = None
        self.imshow_obj = None
        self.colorbar = None
        self.norm = Normalize()
        self.slider_scale_factor = 1.0  
        

        # Create the main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Left side panel
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout, 1)

        # Right side panel
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_layout, 2)

        # Title label
        self.title_label = QLabel("SD SAXS File Viewer")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_layout.addWidget(self.title_label)

        # File type selection
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["All Supported (.tif, .edf)", "TIFF Files (.tif)", "EDF Files (.edf)"])
        self.left_layout.addWidget(self.file_type_combo)
        
        # Lock zoom state toggle
        self.lock_zoom_button = QPushButton("Lock Zoom State: Off")
        self.lock_zoom_button.setCheckable(True)
        self.lock_zoom_button.clicked.connect(self.toggle_zoom_lock)
        self.left_layout.addWidget(self.lock_zoom_button)
        
        # Store the zoom state
        self.zoom_locked = False
        self.current_xlim = None
        self.current_ylim = None

        # Select Folder Button
        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.clicked.connect(self.populate_list)
        self.left_layout.addWidget(self.select_folder_button)

        # List to display files
        self.list_widget = QListWidget()
        self.left_layout.addWidget(self.list_widget)

        # Matplotlib canvas and toolbar
        self.canvas = FigureCanvas(Figure())
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.right_layout.addWidget(self.toolbar)
        self.right_layout.addWidget(self.canvas)

        # Create an axis
        self.ax = self.canvas.figure.subplots()
        self.canvas.figure.patch.set_facecolor('white')
        self.ax.set_facecolor('white')
        self.ax.tick_params(colors='black')
        for spine in self.ax.spines.values():
            spine.set_color('black')

        # Contrast sliders
        self.min_slider = QSlider(Qt.Orientation.Horizontal)
        self.min_slider.setRange(0, 255)
        self.max_slider = QSlider(Qt.Orientation.Horizontal)
        self.max_slider.setRange(0, 255)
        self.left_layout.addWidget(self.min_slider)
        self.left_layout.addWidget(self.max_slider)

        # Number fields to adjust slider range
        self.min_range_field = QLineEdit()
        self.max_range_field = QLineEdit()
        self.left_layout.addWidget(self.min_range_field)
        self.left_layout.addWidget(self.max_range_field)

        # Drop down list for normalization
        self.normalization_combo = QComboBox()
        self.normalization_combo.addItems(["Linear", "Log", "Power"])
        self.normalization_combo.currentIndexChanged.connect(self.handle_normalization_change)
        self.left_layout.addWidget(self.normalization_combo)

        # Drop down list for colormap
        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems([
            "jet","turbo","rainbow","brg","viridis","gnuplot","gnuplot2",
            "inferno","plasma","magma","cividis","YlOrBr","YlOrRd"
        ])
        self.left_layout.addWidget(self.colormap_combo)

        # Connect signals and slots
        self.min_slider.valueChanged.connect(self.update_image)
        self.max_slider.valueChanged.connect(self.update_image)
        self.min_range_field.editingFinished.connect(self.update_slider_range)
        self.max_range_field.editingFinished.connect(self.update_slider_range)
        self.colormap_combo.currentIndexChanged.connect(self.update_image)
        self.list_widget.itemSelectionChanged.connect(self.handle_list_selection)

    def get_file_filter(self):
        selected_type = self.file_type_combo.currentText()
        if selected_type == "TIFF Files (.tif)":
            return [".tif"]
        elif selected_type == "EDF Files (.edf)":
            return [".edf"]
        else:
            return [".tif", ".edf"]

    def populate_list(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.current_dir = folder_path
        try:
            file_extensions = self.get_file_filter()
            supported_files = []
            for f in os.listdir(folder_path):
                if any(f.lower().endswith(ext) for ext in file_extensions):
                    supported_files.append(f)
                    
            if not supported_files:
                raise Exception(f"No supported files found in the selected directory.")
            
            self.list_widget.clear()
            for file_name in supported_files:
                self.list_widget.addItem(file_name)
        except Exception as e:
            self.showError(f"Error populating list: {e}")

    def read_file(self, file_path):
        """Read both TIFF and EDF files."""
        if file_path.lower().endswith('.tif'):
            return tf.imread(file_path)
        elif file_path.lower().endswith('.edf'):
            edf_image = fabio.open(file_path)
            return edf_image.data
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    def handle_list_selection(self):
        try:
            selected_items = self.list_widget.selectedItems()
            if selected_items:
                selected_file = os.path.join(self.current_dir, selected_items[0].text())
                self.current_image = self.read_file(selected_file)
                self.adjust_slider_range(self.current_image)
                self.plot_image()
        except Exception as e:
            self.showError(f"Error in handling list selection: {e}")

    def adjust_slider_range(self, image):
        # Convert numpy values to int to avoid the TypeError
        min_range = int(np.min(image)) + 1
        max_range = int(np.max(image))
        
        # Check if max_range is within QSlider's acceptable range
        # QSlider typically uses int which has a limit around 2^31-1
        INT_MAX = 2147483647  # Maximum value for 32-bit signed integer
        
        if max_range > INT_MAX:
            # Scale down the values to fit within slider range
            scale_factor = max_range / INT_MAX
            min_range = int(min_range / scale_factor)
            max_range = INT_MAX
            # Store the scale factor for later use when updating the image
            self.slider_scale_factor = scale_factor
        else:
            self.slider_scale_factor = 1.0
            
        self.min_slider.setRange(min_range, max_range)
        self.max_slider.setRange(min_range, max_range)
        self.min_range_field.setText(str(min_range * self.slider_scale_factor))
        self.max_range_field.setText(str(max_range * self.slider_scale_factor))

    def plot_image(self):
        # Store current limits if zoom is locked
        if self.zoom_locked:
            self.store_current_view()
            
        self.ax.clear()
        self.ax.set_facecolor('white')
        self.ax.tick_params(colors='black')
        for spine in self.ax.spines.values():
            spine.set_color('black')

        colormap = self.colormap_combo.currentText()
        self.imshow_obj = self.ax.imshow(self.current_image, cmap=colormap, norm=self.norm)
        
        # Restore limits if zoom is locked
        if self.zoom_locked and self.current_xlim is not None and self.current_ylim is not None:
            self.ax.set_xlim(self.current_xlim)
            self.ax.set_ylim(self.current_ylim)

        if self.colorbar is not None:
            try:
                self.colorbar.remove()
            except AttributeError:
                pass

        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)

        self.colorbar = self.canvas.figure.colorbar(self.imshow_obj, cax=cax)

        self.canvas.figure.tight_layout()
        self.canvas.draw()

    def update_image(self):
        min_value = self.min_slider.value() * self.slider_scale_factor
        max_value = self.max_slider.value() * self.slider_scale_factor

        if self.imshow_obj is not None:
            self.imshow_obj.set_clim(vmin=min_value+1e-10, vmax=max_value+1e-10)
            self.imshow_obj.set_cmap(self.colormap_combo.currentText())
            self.canvas.draw()

    def update_slider_range(self):
        try:
            min_range = float(self.min_range_field.text())
            max_range = float(self.max_range_field.text())
            
            if min_range <= 0 or max_range <= 0:
                raise ValueError("Range values must be greater than zero.")
                
            # Calculate scaled slider values
            INT_MAX = 2147483647
            if max_range > INT_MAX:
                scale_factor = max_range / INT_MAX
                self.slider_scale_factor = scale_factor
                scaled_min = int(min_range / scale_factor)
                scaled_max = INT_MAX
            else:
                self.slider_scale_factor = 1.0
                scaled_min = int(min_range)
                scaled_max = int(max_range)
                
            self.min_slider.setRange(scaled_min, scaled_max)
            self.max_slider.setRange(scaled_min, scaled_max)
        except ValueError as ve:
            self.showError(f"Error updating slider range: {ve}")
        except Exception as e:
            self.showError(f"Unexpected error in updating slider range: {e}")

    def toggle_zoom_lock(self):
        """Toggle the zoom lock state."""
        self.zoom_locked = not self.zoom_locked
        self.lock_zoom_button.setText(f"Lock Zoom State: {'On' if self.zoom_locked else 'Off'}")
        
        if self.zoom_locked:
            self.store_current_view()
        else:
            # Reset stored limits when unlocking
            self.current_xlim = None
            self.current_ylim = None
            
    def store_current_view(self):
        """Store the current view limits."""
        if self.ax.get_images():  # Only store if there's an image
            self.current_xlim = self.ax.get_xlim()
            self.current_ylim = self.ax.get_ylim()
            
    def handle_normalization_change(self, index):
        try:
            normalization_dict = {"Linear": Normalize, "Log": LogNorm, "Power": PowerNorm}
            normalization_type = self.normalization_combo.currentText()

            if normalization_type in ["Log", "Power"]:
                self.current_image = np.where(self.current_image <= 0, np.nan, self.current_image)
                self.current_image += 0.0001

            if normalization_type == "Power":
                power, ok = QInputDialog.getDouble(self, "Power Value", "Enter power value:")
                if ok:
                    self.norm = normalization_dict[normalization_type](power)
                else:
                    self.normalization_combo.setCurrentIndex(index - 1)
            else:
                self.norm = normalization_dict[normalization_type]()

            self.plot_image()
        except Exception as e:
            self.showError(f"Error in normalization: {e}")

def main():
    app = QApplication(sys.argv)
    window = SDFileViewer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()