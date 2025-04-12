import numpy as np
import pandas as pd
from napari.layers import Labels
from qtpy.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MaskAnalyzer(QWidget):
    """Widget for analyzing mask density in selected regions."""

    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        # Set up the UI
        layout = QVBoxLayout()
        self.setLayout(layout)

        # MPP input field
        mpp_layout = QHBoxLayout()
        mpp_layout.addWidget(QLabel("Microns Per Pixel (μm/px):"))
        self.mpp_input = QLineEdit("0.5")  # Default value of 0.5
        self.mpp_input.setMaximumWidth(100)
        mpp_layout.addWidget(self.mpp_input)
        layout.addLayout(mpp_layout)

        # Multi-selection list for mask layers instead of dropdown
        layout.addWidget(QLabel("Select Mask Layer(s):"))
        self.mask_list = QListWidget()
        self.mask_list.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(self.mask_list)

        # Button to update mask layer options
        update_btn = QPushButton("Update Layer List")
        update_btn.clicked.connect(self.update_mask_layers)
        layout.addWidget(update_btn)

        # Button to add a selection shape
        add_roi_btn = QPushButton("Add Selection ROI")
        add_roi_btn.clicked.connect(self.add_selection_roi)
        layout.addWidget(add_roi_btn)

        # Button to analyze selection
        analyze_btn = QPushButton("Analyze Selected Region")
        analyze_btn.clicked.connect(self.analyze_selection)
        layout.addWidget(analyze_btn)

        # Results display
        self.results_label = QLabel("Results will appear here")
        self.results_label.setWordWrap(True)  # Allow wrapping long text
        layout.addWidget(self.results_label)

        # Export button
        export_btn = QPushButton("Export Results to CSV")
        export_btn.clicked.connect(self.export_results)
        layout.addWidget(export_btn)

        # Initialize layer list
        self.update_mask_layers()
        self.results = []  # Changed to a list for multiple selections

        # Connect to layer list changes
        self.viewer.layers.events.inserted.connect(self.update_mask_layers)
        self.viewer.layers.events.removed.connect(self.update_mask_layers)

    def update_mask_layers(self, event=None):
        """Update the list widget with available mask layers."""
        self.mask_list.clear()
        for layer in self.viewer.layers:
            if isinstance(layer, Labels):
                self.mask_list.addItem(layer.name)

    def add_selection_roi(self):
        """Add a shape layer for region selection if it doesn't exist."""
        if "ROI Selection" not in self.viewer.layers:
            self.viewer.add_shapes(
                name="ROI Selection",
                face_color="transparent",
                edge_color="yellow",
                opacity=0.5,
            )
        self.viewer.layers["ROI Selection"].mode = "add_rectangle"

    def analyze_selection(self):
        """Analyze the masks within the selected region."""
        # Get the MPP value
        try:
            mpp = float(self.mpp_input.text())
            if mpp <= 0:
                raise ValueError("MPP must be positive")
        except ValueError:
            self.results_label.setText(
                "Please enter a valid positive number for MPP"
            )
            return

        # Get the selected mask layers
        selected_items = self.mask_list.selectedItems()
        if not selected_items:
            self.results_label.setText("Please select at least one mask layer")
            return

        selected_masks = [item.text() for item in selected_items]

        # Get the selection layer
        if "ROI Selection" not in self.viewer.layers:
            self.results_label.setText("Please create a selection first")
            return

        roi_layer = self.viewer.layers["ROI Selection"]
        if len(roi_layer.data) == 0:
            self.results_label.setText("Please create a selection first")
            return

        # Get the most recent selection
        roi = roi_layer.data[-1]

        # Reset results list for this analysis
        self.results = []

        # Process each selected mask
        result_text = "Analysis Results:\n"

        for mask_name in selected_masks:
            mask_layer = self.viewer.layers[mask_name]
            mask_data = mask_layer.data

            # Get dimensions of the mask
            h, w = mask_data.shape

            # Convert roi vertices to integers
            roi_int = roi.astype(int)

            # Get min and max coordinates for the bounding box
            min_y, min_x = np.min(roi_int, axis=0)
            max_y, max_x = np.max(roi_int, axis=0)

            # Ensure coordinates are within image bounds
            min_y = max(0, min_y)
            min_x = max(0, min_x)
            max_y = min(h, max_y)
            max_x = min(w, max_x)

            # Create region mask
            region_mask = np.zeros((h, w), dtype=bool)
            region_mask[min_y:max_y, min_x:max_x] = True

            # Apply region mask to the cell mask
            masked_cells = mask_data * region_mask

            # Count unique cell ids (excluding 0 which is background)
            unique_cells = np.unique(masked_cells)
            unique_cells = unique_cells[unique_cells > 0]
            num_cells = len(unique_cells)

            # Calculate region area
            region_area_pixels = (max_y - min_y) * (max_x - min_x)
            region_area_microns = region_area_pixels * (
                mpp**2
            )  # Convert to μm²

            # Calculate density (cells per μm²)
            density_per_micron = (
                num_cells / region_area_microns if region_area_microns else 0
            )

            # Store results for this mask
            mask_result = {
                "ROI": len(roi_layer.data),
                "Mask Layer": mask_name,
                "Number of Masks": num_cells,
                "MPP (μm/px)": mpp,
                "Region Area (pixels)": region_area_pixels,
                "Region Area (μm²)": region_area_microns,
                "Density (masks/μm²)": density_per_micron,
            }

            self.results.append(mask_result)

            # Add to result text
            result_text += f"\n{mask_name}:\n"
            result_text += f"  Number of masks: {num_cells}\n"
            result_text += f"  Area: {region_area_microns:.2f} μm²\n"
            result_text += f"  Density: {density_per_micron:.6f} masks/μm²\n"

        # Display results
        self.results_label.setText(result_text)

        # Add results as a layer property
        if not hasattr(roi_layer, "analysis_results"):
            roi_layer.analysis_results = []
        roi_layer.analysis_results.extend(self.results)

    def export_results(self):
        """Export analysis results to CSV."""
        if "ROI Selection" not in self.viewer.layers:
            self.results_label.setText("No ROI Selection layer found.")
            return

        if not hasattr(
            self.viewer.layers["ROI Selection"], "analysis_results"
        ):
            self.results_label.setText("No analysis results to export")
            return

        results = self.viewer.layers["ROI Selection"].analysis_results

        if not results:
            self.results_label.setText("No analysis results to export")
            return

        # Convert results to DataFrame
        df = pd.DataFrame(results)

        # Ask for save location
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Results", "", "CSV Files (*.csv)"
        )

        if filepath:
            df.to_csv(filepath, index=False)
            # Show only the filename part without the full path to avoid UI width issues
            filename = filepath.split("/")[-1]
            self.results_label.setText(f"Results saved to: {filename}")
