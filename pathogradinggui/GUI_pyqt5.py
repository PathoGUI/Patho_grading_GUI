from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDoubleSpinBox, QGridLayout, QWidget, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QAction, QComboBox,
    QSpacerItem, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QFormLayout,
    )
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import pandas as pd
import csv
from user_auth import UserDatabase
import sys
from login_dialog import LoginDialog, show_login_dialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        ############# Layout #####################
        # sshFile="stylesheet.css"
        # with open(sshFile,"r") as fh:
        #     self.setStyleSheet(fh.read())
        
        self.current_user = None
        self.setWindowTitle("PathoGUI")

        # Create layout for the UI
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Create a matplotlib figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)        

        # Add x,y,z coordinate display
        self.x_coordinate_textbox = QLineEdit()
        self.x_coordinate_textbox.setReadOnly(True)
        self.y_coordinate_textbox = QLineEdit()
        self.y_coordinate_textbox.setReadOnly(True)
        self.arrayshape_textbox = QLineEdit()
        self.arrayshape_textbox.setReadOnly(True)
        form_layout = QFormLayout()
        form_layout.addRow("x-coordinate:", self.x_coordinate_textbox)
        form_layout.addRow("y-coordinate:", self.y_coordinate_textbox)
        form_layout.addRow("Annotation:", self.arrayshape_textbox)
        coordinates_container = QGroupBox("Coordinates")
        coordinates_container.setLayout(form_layout)

        # Add Contrast enhancement for cyto channel
        self.default_cyto_clip_lower = 0
        self.default_cyto_clip_higher = 1200
        dropdown_layout1 = QVBoxLayout()
        dropdown_layout1.addWidget(QLabel("Primary grade:"))
        self.dropdown1 = QComboBox()
        self.dropdown1.addItem("3")
        self.dropdown1.addItem("4")
        self.dropdown1.addItem("5")
        dropdown_layout1.addWidget(self.dropdown1)
        dropdown_layout1.addWidget(QLabel("Secondary grade:"))
        self.dropdown1 = QComboBox()
        self.dropdown1.addItem("3")
        self.dropdown1.addItem("4")
        self.dropdown1.addItem("5")
        dropdown_layout1.addWidget(self.dropdown1)

        dropdown_container1 = QGroupBox("Grading")
        dropdown_container1.setLayout(dropdown_layout1)

        # Button to save all the settings
        save_button = QPushButton("Save and Next")
        save_button.clicked.connect(self.save_coords)
        # Home button to show the entire image
        home_button = QPushButton("Clear all")
        button_layout = QHBoxLayout()
        button_layout.addWidget(home_button)
        button_layout.addWidget(save_button)
        button_layout.addStretch()

        # Configure left layout and right layout and make it central
        left_layout.addWidget(self.canvas)
        left_layout.addWidget(self.toolbar)
        right_layout.addWidget(coordinates_container)
        right_layout.addWidget(dropdown_container1)
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



if __name__ == '__main__':
    app = QApplication([])

    # Initialize the user database
    user_db = UserDatabase()

    # Show the login dialog
    current_user = show_login_dialog(user_db, MainWindow)

    # Now, only if authentication is successful, create and show the main window
    if current_user:
        w = MainWindow()
        w.current_user = current_user  # Set the current user
        w.show()
        sys.exit(app.exec_())