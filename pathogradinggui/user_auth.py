"""
PyQt5 Application with User Authentication

This module provides a simple PyQt5-based application that includes user authentication.
It utilizes a UserDatabase class for managing user information and a GUI with a main window
and a login dialog for user authentication.

Dependencies:
- PyQt5: The Qt toolkit for Python.
- users.User: A module containing the UserDatabase class for managing user information.
- GUI_pyqt5.MainWindow: A module containing the MainWindow class for the main application window.
- login_dialog: A module containing the show_login_dialog function for displaying the login dialog.

Usage:
1. Run this module as the main script to start the application.
2. The application initializes a PyQt5 QApplication.
3. It creates an instance of the UserDatabase class to manage user information.
4. The login dialog is shown using the show_login_dialog function, which takes the user database
   as a parameter and returns the authenticated user if successful.
5. If authentication is successful, the main window is created with the authenticated user.
6. The login dialog is shown again with the main window as a parent, ensuring it is modal.
7. The application runs the event loop until the user exits the main window.

Note: Make sure to customize the UserDatabase class to fit the
specific requirements of your application.
"""
from PyQt5.QtWidgets import QApplication
import sys
#sys.path.append("./users")
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from users.User import UserDatabase
from GUI_pyqt5 import MainWindow
from login_dialog import show_login_dialog

if __name__ == '__main__':
    app = QApplication([])

    # Initialize the user database
    user_db = UserDatabase()

    # Show the login dialog
    current_user = show_login_dialog(user_db)

    # Now, only if authentication is successful,
    # create and show the main window
    if current_user:
        w = MainWindow(current_user)
        show_login_dialog(user_db, w)
        sys.exit(app.exec_())
