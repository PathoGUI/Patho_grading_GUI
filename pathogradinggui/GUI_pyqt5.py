import csv
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDoubleSpinBox, QGridLayout, QWidget, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QAction, QComboBox,
    QSpacerItem, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QFormLayout,
    )
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import pandas as pd
from user_auth import UserDatabase
import sys
import os
from login_dialog import LoginDialog, show_login_dialog
import time
import datetime


class MainWindow(QMainWindow):
    """Main window for the application."""
    def __init__(self, current_user):
        super().__init__()

        """Initialize the main window."""
        
        # sshFile="stylesheet.css"
        # with open(sshFile,"r") as fh:
        #     self.setStyleSheet(fh.read())

        self.current_user = None
        self.setWindowTitle("PathoGUI")

        # Load images and initialize image index
        """ Select only image file starts with 'S' and ends with '.tif' to prevent error"""

        image_path_list = []
        for element in os.listdir("../Data"):
            if element.startswith("S") and element.endswith('.tif'):
                image_path_list.append(element)
        self.image_paths = image_path_list
        self.image_index = 0
        self.canvas = None
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)   
        self.load_image() 


        ######################## UI Layout ##################################
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Add user name display, loading label
        self.user_name = QLineEdit()
        self.user_name.setReadOnly(True)
        self.user_name.setStyleSheet("background-color: #f0f0f0;")
        self.user_name.setText(current_user)        
        self.form_layout_0 = QFormLayout()
        self.form_layout_0.addRow("Logged in as:", self.user_name)
        self.loading_label = QLabel()

        # Add x,y,z coordinate display
        self.x_coordinate_textbox = QLineEdit()
        self.x_coordinate_textbox.setReadOnly(True)
        self.x_coordinate_textbox.setStyleSheet("background-color: #f0f0f0;")
        self.y_coordinate_textbox = QLineEdit()
        self.y_coordinate_textbox.setReadOnly(True)
        self.y_coordinate_textbox.setStyleSheet("background-color: #f0f0f0;")
        self.comment_textbox = QLineEdit()
        form_layout = QFormLayout()
        form_layout.addRow("x-coordinate:", self.x_coordinate_textbox)
        form_layout.addRow("y-coordinate:", self.y_coordinate_textbox)
        form_layout.addRow("Comments:", self.comment_textbox)
        coordinates_container = QGroupBox("Coordinates")
        coordinates_container.setLayout(form_layout)

        # Add Primary and Secondary grades dropdown manual
        dropdown_layout = QVBoxLayout()
        dropdown_layout.addWidget(QLabel("Primary grade:"))
        self.dropdown1 = QComboBox()
        self.dropdown1.addItem("3")
        self.dropdown1.addItem("4")
        self.dropdown1.addItem("5")
        dropdown_layout.addWidget(self.dropdown1)
        dropdown_layout.addWidget(QLabel("Secondary grade:"))
        self.dropdown2 = QComboBox()
        self.dropdown2.addItem("3")
        self.dropdown2.addItem("4")
        self.dropdown2.addItem("5")
        dropdown_layout.addWidget(self.dropdown2)
        dropdown_container = QGroupBox("Grading")
        dropdown_container.setLayout(dropdown_layout)

        # Create "Previous" and "Next" buttons
        previous_button = QPushButton("Previous")
        previous_button.clicked.connect(self.previous_image)
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_image)
        # Button to save all the settings
        save_button = QPushButton("Save")
        save_button.setStyleSheet("QPushButton {background-color: green; color: white; }")
        save_button.clicked.connect(self.save_coords)
        # Home button to show the entire image
        home_button = QPushButton("Clear all")
        button_layout = QHBoxLayout()
        button_layout.addWidget(home_button)
        button_layout.addWidget(previous_button)
        button_layout.addWidget(next_button)
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        

        # Configure left layout and right layout and make it central
        left_layout.addWidget(self.canvas)
        left_layout.addWidget(self.toolbar)
        right_layout.addLayout(self.form_layout_0)
        right_layout.addWidget(self.loading_label)
        right_layout.addWidget(coordinates_container)
        right_layout.addWidget(dropdown_container)
        right_layout.addLayout(button_layout)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.cid = None

        ############# End of Layout ######################################

    """
    Backend functions: 
        - save_coords(): 
        - load_image():
        - previous_image():
        - next_image():

    """
    def show_saving(self):
        self.loading_label.setText("Saving...")
        self.loading_label.setStyleSheet("color: green;")
        QApplication.processEvents()


    def hide_text(self):
        self.loading_label.clear()
        QApplication.processEvents()


    def save_coords(self):
        """
        This function..
        - retrieves all the values to be saved
        - write it into a .csv file when "Save" button is clicked
        """
        self.show_saving()

        PrimaryGrade   = self.dropdown1.currentText()
        SecondaryGrade = self.dropdown2.currentText()
        image_name     = self.image_name
        user_name      = self.user_name.text()
        dt             = str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

        headers = ["Date&Time", "User", "Image name", "PrimaryGrade", "SecondaryGrade"]
        values =  [dt, user_name, image_name, PrimaryGrade, SecondaryGrade]

        root_folder = "./Results"
        if not os.path.exists(root_folder):
            os.mkdir(root_folder)
        filename = root_folder + os.sep + "Grading_result_" + self.user_name.text() + ".csv"
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(headers)
            writer.writerow(values)

        time.sleep(0.5)
        self.hide_text()


    def load_image(self):
        """Load and display the current image."""
        if 0 <= self.image_index < len(self.image_paths):
            self.image_name = self.image_paths[self.image_index]
            img = mpimg.imread('../Data/' + self.image_name)

            # Clear the existing axes
            self.figure.clear()
            self.ax = self.figure.add_subplot(1, 1, 1)
            self.ax.imshow(img)
            self.ax.set_title(self.image_name)
            ax = self.figure.gca()
            self.x_limits = ax.get_xlim()
            self.y_limits = ax.get_ylim()

            self.canvas.draw_idle()

    def previous_image(self):
        """Show the previous image."""
        if self.image_index > 0:
            self.image_index -= 1
            self.load_image()

    def next_image(self):
        """Show the next image."""
        if self.image_index < len(self.image_paths) - 1:
            self.image_index += 1
            self.load_image()



if __name__ == '__main__':
    app = QApplication([])

    # Initialize the user database
    user_db = UserDatabase()

    # Show the login dialog
    current_user = show_login_dialog(user_db, MainWindow)

    # Now, only if authentication is successful, create and show the main window
    if current_user:
        w = MainWindow(current_user)
        w.current_user = current_user  # Set the current user
        w.show()
        sys.exit(app.exec_())