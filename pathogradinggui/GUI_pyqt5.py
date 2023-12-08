""" Module providing a function creating CSV file"""
import sys
import os
import csv
import time
import datetime
import matplotlib.image as mpimg

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QPushButton,
    QLabel,QComboBox,
    QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QFormLayout,
    )
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from user_auth import UserDatabase
from login_dialog import LoginDialog, show_login_dialog

class MainWindow(QMainWindow):
    """Main window for the application."""
    def __init__(self, current_user):
        """Initialize the main window."""
        super().__init__()
        self.current_user = None
        self.setWindowTitle("PathoGUI")

        # Load images and initialize image index
        image_path_list = []
        for element in os.listdir("../Data"):
            if element.startswith("S") and element.endswith('.tif'):
                image_path_list.append(element)
        self.image_paths = image_path_list
        self.image_index = 0
        self.canvas = None
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('button_release_event', self.on_zoom_completed)

        self.toolbar = NavigationToolbar(self.canvas, self)

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
        self.dropdown1.addItem(" ")
        self.dropdown1.addItem("3")
        self.dropdown1.addItem("4")
        self.dropdown1.addItem("5")
        dropdown_layout.addWidget(self.dropdown1)
        dropdown_layout.addWidget(QLabel("Secondary grade:"))
        self.dropdown2 = QComboBox()
        self.dropdown2.addItem(" ")
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
        # Clear button to clear all input
        clear_button = QPushButton("Clear all")
        clear_button.clicked.connect(self.clear_input)
        button_layout = QHBoxLayout()
        button_layout.addWidget(clear_button)
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
        self.load_image()

        ############# End of Layout ######################################

    def on_zoom_completed(self, event):
        """ Redraw figure when user zooming"""
        if event.name == 'button_release_event':
            self.figure.canvas.mpl_disconnect(self.cid)
            self.cid = self.figure.canvas.mpl_connect('draw_event', self.on_draw_completed)

    def on_draw_completed(self, event):
        """ Show coordinate after user finished drawing"""
        self.figure.canvas.mpl_disconnect(self.cid)
        axes = self.figure.gca()
        x_limits = self.x_limits
        y_limits = self.y_limits
        if axes:
            # Don't let it pan out of bound
            x_limits = axes.get_xlim()
            y_limits = axes.get_ylim()

        self.x_limits = x_limits
        self.y_limits = y_limits

        self.x_coordinate_textbox.setText(str(format(self.x_limits[0],".3f")))
        self.y_coordinate_textbox.setText(str(format(self.y_limits[1],".3f")))

        self.x_coordinate_textbox.update()
        self.y_coordinate_textbox.update()


    def show_saving(self):
        """ Show status when user click save button"""
        self.loading_label.setText("Saving...")
        self.loading_label.setStyleSheet("color: green;")
        QApplication.processEvents()


    def hide_text(self):
        """ Clear status when saving has been done"""
        self.loading_label.clear()
        QApplication.processEvents()


    def save_coords(self):
        """
        This function..
        - retrieves all the values to be saved
        - write it into a .csv file when "Save" button is clicked
        """
        self.show_saving()

        primary_grade   = self.dropdown1.currentText()
        secondary_grade = self.dropdown2.currentText()
        x_coord    = self.x_coordinate_textbox.text()
        y_coord    = self.y_coordinate_textbox.text()
        image_name     = self.image_name
        user_name      = self.user_name.text()
        dt_             = str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

        headers = ["Date&Time", "User", "Image name",
                   "PrimaryGrade", "SecondaryGrade", "xcoord", "ycoord"]
        values =  [dt_, user_name, image_name, primary_grade, secondary_grade, x_coord, y_coord]

        root_folder = "./Results"
        if not os.path.exists(root_folder):
            os.mkdir(root_folder)
        filename = root_folder + os.sep + "Grading_result_" + self.user_name.text() + ".csv"
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
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

            img_title = "Biopsy name: " + self.image_name.split(".tif")[0]

            # Clear the existing axes
            self.figure.clear()
            self.axes = self.figure.add_subplot(1, 1, 1)
            self.axes.imshow(img)
            self.axes.set_title(img_title)
            self.axes.spines['right'].set_visible(False)
            self.axes.spines['top'].set_visible(False)
            axes = self.figure.gca()
            self.x_limits = axes.get_xlim()
            self.y_limits = axes.get_ylim()
            self.x_coordinate_textbox.setText(str(format(self.x_limits[0],".3f")))
            self.y_coordinate_textbox.setText(str(format(self.y_limits[1],".3f")))
            self.x_coordinate_textbox.update()
            self.y_coordinate_textbox.update()

            self.canvas.draw_idle()

    def previous_image(self):
        """Show the previous image."""
        self.clear_input()
        if self.image_index > 0:
            self.image_index -= 1
            self.load_image()
            self.comment_textbox.clear()

    def next_image(self):
        """Show the next image."""
        self.clear_input()
        if self.image_index < len(self.image_paths) - 1:
            self.image_index += 1
            self.load_image()
            self.comment_textbox.clear()

    def clear_input(self):
        """Clear input"""
        self.comment_textbox.clear()
        self.dropdown1.setCurrentText(" ")
        self.dropdown2.setCurrentText(" ")

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
