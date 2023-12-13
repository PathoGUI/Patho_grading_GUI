"""
Testing GUI_pyqt5.py for the following function
1) test_load_image (smoke test)
2) test_clear_input (one-shot test)
3) test_save_coords (one-shot test)
4) test_load_image_unsupported_type (Edge test)

NOTE (12/10/23) test all functions at the same time resulted in 'Segmentation fault' warning
This file supports only one test per run
please comment out the rest of three functions to test it (using ''' ... ''') (start from line 69)
to run test >> python GUI_pyqt5_test.py
"""
import unittest
import os
import shutil
import tempfile
import pytest

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QPushButton,
    QLabel,QComboBox,
    QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QFormLayout,
    )
from matplotlib.backends.backend_qt5agg import (FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from user_auth import UserDatabase
from login_dialog import LoginDialog, show_login_dialog

from GUI_pyqt5 import MainWindow

class TestMainWindow(unittest.TestCase):
    """ This class manges the test for Patho GUI application"""
    
    
    skip1 = pytest.importorskip('user_auth.skip1')
    skip2 = pytest.importorskip('login_dialog.skip2')

    

    def setUp(self):
        """Set up the test environment."""
        self.app = QApplication([])
        self.main_window = MainWindow("test_user")

        # Prepare fake image for test_load_image_unsupported_typ function
        # 1) Create a temporary image file
        temp_image_fd, temp_image_path = tempfile.mkstemp(suffix=".png")
        os.close(temp_image_fd)

        # 2) Destination path in the "Data" folder
        data_folder_path = os.path.join(os.getcwd(), "Data_temp")
        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)
        dest_image_path = os.path.join(data_folder_path, "temp_image.png")

        # 3) Copy or move the temporary image to the "Data" folder
        shutil.copy(temp_image_path, dest_image_path)

        # 4) Set the image paths in MainWindow for testing
        self.main_window.image_paths = ["temp_image.png"]

    def tearDown(self):
        """Clean up after the test."""
        self.app.quit()

        # Delete the generated CSV file (creat in test_save_coords function)
        file_path = 'Results/Grading_result_test_user.csv'
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete the Data_temp folder and its content 
        # (creat in test_load_image_unsupported_type function)
        data_folder_path = os.path.join(os.getcwd(), "Data_temp")
        if os.path.exists(data_folder_path):
            shutil.rmtree(data_folder_path)

    # Start test function from here:

    def test_load_image(self):
        """ Smoke test to test if the first image appear with load_image() function"""
        self.main_window = MainWindow("test_user")

        # Set the image index to a specific value for testing
        self.main_window.image_index = 1

        # Call the load_image function
        self.main_window.load_image()

        # Assert that the image name has been set correctly
        self.assertEqual(self.main_window.image_name, "S128_A.tif")

    def test_clear_input(self):
        """ One-shot test to test if clear_input() function does clear text& drop down input"""
        # Create an instance of MainWindow
        main_window = MainWindow("test_user")

        # Mock some data in the comment textbox, dropdowns, etc.
        main_window.comment_textbox.setText("Some comment")
        main_window.dropdown1.setCurrentText("3")
        main_window.dropdown2.setCurrentText("4")

        # Call the clear_input function
        main_window.clear_input()

        # Check if the values are cleared
        self.assertEqual(main_window.comment_textbox.text(), "")
        self.assertEqual(main_window.dropdown1.currentText(), " ")
        self.assertEqual(main_window.dropdown2.currentText(), " ")

    def test_save_coords(self):
        """ One-shot test to test if save_coords() function save the correct output as CSV file
        note: ignore date&time column as time generated within the test_save_coords
        are slightly different (+/- 0.01 second) which leads to error when perform assertEqual"""
        # Mock user input
        primary_grade_input = '3'
        secondary_grade_input = '4'
        x_coord_input = '10.123'
        y_coord_input = '20.456'
        image_name = 'test_image.tif'
        user_name = 'test_user'

        # Create an instance of MainWindow with mocked inputs
        window = MainWindow(user_name)
        window.dropdown1.setCurrentText(primary_grade_input)
        window.dropdown2.setCurrentText(secondary_grade_input)
        window.x_coordinate_textbox.setText(x_coord_input)
        window.y_coordinate_textbox.setText(y_coord_input)
        window.image_name = image_name
        window.user_name.setText(user_name)

        # Call the save_coords function
        window.save_coords()

        # Assert that the CSV file is created with the expected values
        # ignore date&time column in expected_csv_content file
        expected_csv_content = (
            "User,Image name,PrimaryGrade,SecondaryGrade,xcoord,ycoord\n"
            "test_user,test_image.tif,3,4,10.123,20.456\n"
        )

        # ignore date&time column in actual_csv_content file
        with open('Results/Grading_result_test_user.csv', 'r', encoding='utf-8') as file:
            actual_csv_content = file.read()

        # Split the content into rows
        rows = actual_csv_content.split('\n')

        # Remove the first column from each row
        actual_csv_content = '\n'.join(','.join(row.split(',')[1:]) for row in rows)

        # Assert that expected content is same as actual content
        self.assertEqual(actual_csv_content, expected_csv_content)

        # Assert that the loading label was cleared
        self.assertEqual(window.loading_label.text(), '')

    def test_load_image_unsupported_type(self):
        """ Load fake .png image to test if the module is able to cathc error"""
        # Set the image index to an unsupported image type for testing
        self.main_window.image_index = 0  # The first image is an unsupported type

        # Call the load_image function
        with self.assertRaises(Exception):
            self.main_window.load_image()

if __name__ == '__main__':
    unittest.main()
