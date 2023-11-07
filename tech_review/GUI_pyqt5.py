from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDoubleSpinBox, QGridLayout, QWidget, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QAction, QComboBox,
    QSpacerItem, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QFormLayout
)
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import pandas as pd
import csv


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

             ############# Layout #####################

        self.setWindowTitle("ROI Preview")

        # Create layout for the UI
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Create a matplotlib figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)        

        # Add button to change between channels
        button_layout = QHBoxLayout()
        cyto_button = QPushButton("Cyto")
        button_layout.addWidget(cyto_button)
        nuc_button = QPushButton("Nuc")
        button_layout.addWidget(nuc_button)
        target_button = QPushButton("Target")
        button_layout.addWidget(target_button)
        button_container = QGroupBox("Channels")
        button_container.setLayout(button_layout)
        self.setCentralWidget(button_container)

        # Add x,y,z coordinate display
        self.x_coordinate_textbox = QLineEdit()
        self.x_coordinate_textbox.setReadOnly(True)
        self.y_coordinate_textbox = QLineEdit()
        self.y_coordinate_textbox.setReadOnly(True)
        self.arrayshape_textbox = QLineEdit()
        self.arrayshape_textbox.setReadOnly(True)
        self.current_z_level_textbox = QLineEdit()
        self.current_z_level_textbox.setReadOnly(True)
        form_layout = QFormLayout()
        form_layout.addRow("x-coordinate:", self.x_coordinate_textbox)
        form_layout.addRow("y-coordinate:", self.y_coordinate_textbox)
        form_layout.addRow("Current Z-Level:", self.current_z_level_textbox)
        form_layout.addRow("Vol Shape:", self.arrayshape_textbox)
        coordinates_container = QGroupBox("Coordinates")
        coordinates_container.setLayout(form_layout)

        # Add Contrast enhancement for cyto channel
        self.default_cyto_clip_lower = 0
        self.default_cyto_clip_higher = 1200
        dropdown_layout1 = QVBoxLayout()
        dropdown_layout1.addWidget(QLabel("Contrast Enhancement Method:"))
        self.dropdown1 = QComboBox()
        self.dropdown1.addItem("Rescale")
        self.dropdown1.addItem("CLAHE")
        dropdown_layout1.addWidget(self.dropdown1)
        clip_high_layout1 = QHBoxLayout()
        clip_high_layout1.addWidget(QLabel("Clip High:"))
        self.ClipHighLim_cyto = QDoubleSpinBox()
        self.ClipHighLim_cyto.setRange(0, 4500)
        self.ClipHighLim_cyto.setSingleStep(50)
        self.ClipHighLim_cyto.setValue(self.default_cyto_clip_higher)
        clip_high_layout1.addWidget(self.ClipHighLim_cyto)
        clip_low_layout1 = QHBoxLayout()
        clip_low_layout1.addWidget(QLabel("Clip Low:"))
        self.ClipLowLim_cyto = QDoubleSpinBox()
        self.ClipLowLim_cyto.setRange(0, 4500)
        self.ClipLowLim_cyto.setSingleStep(50)
        self.ClipLowLim_cyto.setValue(self.default_cyto_clip_lower)

        clip_low_layout1.addWidget(self.ClipLowLim_cyto)
        dropdown_layout1.addLayout(clip_high_layout1)
        dropdown_layout1.addLayout(clip_low_layout1)
        dropdown_container1 = QGroupBox("Cyto")
        dropdown_container1.setLayout(dropdown_layout1)

        # Add Contrast enhancement for Nuc channel
        dropdown_layout2 = QVBoxLayout()
        dropdown_layout2.addWidget(QLabel("Contrast Enhancement Method:"))
        dropdown2 = QComboBox()
        dropdown2.addItem("Rescale")
        dropdown2.addItem("CLAHE")
        dropdown_layout2.addWidget(dropdown2)
        clip_high_layout2 = QHBoxLayout()
        clip_high_layout2.addWidget(QLabel("Clip High:"))
        self.ClipHighLim_nuc = QDoubleSpinBox()
        self.ClipHighLim_nuc.setRange(0, 4500)
        self.ClipHighLim_nuc.setSingleStep(50)
        self.ClipHighLim_nuc.setValue(2000)
        clip_high_layout2.addWidget(self.ClipHighLim_nuc)
        clip_low_layout2 = QHBoxLayout()
        clip_low_layout2.addWidget(QLabel("Clip Low:"))
        self.ClipLowLim_nuc = QDoubleSpinBox()
        self.ClipLowLim_nuc.setRange(0, 4500)
        self.ClipLowLim_nuc.setSingleStep(50)
        self.ClipLowLim_nuc.setValue(0)

        clip_low_layout2.addWidget(self.ClipLowLim_nuc)
        dropdown_layout2.addLayout(clip_high_layout2)
        dropdown_layout2.addLayout(clip_low_layout2)
        dropdown_container2 = QGroupBox("Nuc")
        dropdown_container2.setLayout(dropdown_layout2)

        # Add Contrast enhancement for Target channel
        dropdown_layout3 = QVBoxLayout()
        dropdown_layout3.addWidget(QLabel("Contrast Enhancement Method:"))
        dropdown3 = QComboBox()
        dropdown3.addItem("Rescale")
        dropdown3.addItem("CLAHE")
        dropdown_layout3.addWidget(dropdown3)
        clip_high_layout3 = QHBoxLayout()
        clip_high_layout3.addWidget(QLabel("Clip High:"))
        self.ClipHighLim_pgp = QDoubleSpinBox()
        self.ClipHighLim_pgp.setRange(0, 4500)
        self.ClipHighLim_pgp.setSingleStep(50)
        self.ClipHighLim_pgp.setValue(700)
        clip_high_layout3.addWidget(self.ClipHighLim_pgp)
        clip_low_layout3 = QHBoxLayout()
        clip_low_layout3.addWidget(QLabel("Clip Low:"))
        self.ClipLowLim_pgp = QDoubleSpinBox()
        self.ClipLowLim_pgp.setRange(0, 4500)
        self.ClipLowLim_pgp.setSingleStep(50)
        self.ClipLowLim_pgp.setValue(0)

        clip_low_layout3.addWidget(self.ClipLowLim_pgp)
        dropdown_layout3.addLayout(clip_high_layout3)
        dropdown_layout3.addLayout(clip_low_layout3)
        dropdown_container3 = QGroupBox("Target")
        dropdown_container3.setLayout(dropdown_layout3)

        # Button to save all the settings
        save_button = QPushButton("Save params")
        save_button.clicked.connect(self.save_coords)
        # Home button to show the entire image
        home_button = QPushButton("Home")
        button_layout = QHBoxLayout()
        button_layout.addWidget(home_button)
        button_layout.addWidget(save_button)
        button_layout.addStretch()

        # Configure left layout and right layout and make it central
        left_layout.addWidget(self.canvas)
        left_layout.addWidget(self.toolbar)
        left_layout.addWidget(button_container)
        right_layout.addWidget(coordinates_container)
        right_layout.addWidget(dropdown_container1)
        right_layout.addWidget(dropdown_container2)
        right_layout.addWidget(dropdown_container3)
        right_layout.addLayout(button_layout)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.cid = None

        ############# End of Layout ######################################

        

    def save_coords(self):
        # Retrieve values for shapes and current z level
        shape = self.arrayshape_textbox.text()
        currentZ = self.current_z_level_textbox.text()

        # Retrieve values from clipvalues
        nuc_cliplow = self.clip_higher_limit1.value()
        # nuc_cliphigh = 
        # cyto_cliplow = 
        # cyto_cliphigh = 
        # pgp_cliplow = 
        # pgp_cliphigh = 

        # Retrieve method used for contrast enhancement
        nuc_ctehmt_method = self.dropdown1.currentText()
        # cyto_ctehmt_method = 
        # pgp_ctehmt_method = 


        filename = "ROI_coords_.csv"
        headers = ["Shape", "Current Z level", "nuc clip","nuc CE method"]
        values = [shape, currentZ, nuc_cliplow, nuc_ctehmt_method]
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(headers)
            writer.writerow(values)

        # # Create a dictionary to store the values
        # data = {
        #     'LineEditValue1': [shape],
        #     'LineEditValue2': [currentZ],
        #     # ... add more key-value pairs for other widgets
        # }

        # # Convert the data dictionary to a pandas DataFrame
        # df = pd.DataFrame(data)

        # # Check if the Excel file already exists
        # try:
        #     # Load the existing file and append the DataFrame to it
        #     book = load_workbook('settings.xlsx')
        #     writer = pd.ExcelWriter('settings.xlsx', engine='openpyxl')
        #     writer.book = book
        #     writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        #     startrow = writer.sheets['Sheet1'].max_row
        #     df.to_excel(writer, sheet_name='Sheet1', startrow=startrow, index=False, header=False)
        #     writer.save()
        #     writer.close()
        # except FileNotFoundError:
        #     # If the file doesn't exist, create a new one with the DataFrame
        #     df.to_excel('settings.xlsx', index=False)



app = QApplication([])
w = MainWindow()
w.show()
app.exec()