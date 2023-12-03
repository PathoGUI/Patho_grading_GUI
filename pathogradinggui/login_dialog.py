"""
Module: login_dialog.py

This module defines a PyQt5-based login dialog for user authentication
and new user creation.
It includes a LoginDialog class that inherits from QDialog and
provides the following features:
- Username and password input fields with labels
- Login and Create New User buttons with corresponding actions
- Authentication against a user database (provided during initialization)
- Handling and display of error and information messages using QMessageBox
- Optionally linked to a main window for integration into larger applications

The module also includes a function `show_login_dialog` that creates
an instance of LoginDialog,
displays it, and returns the authenticated user on successful login.

Usage:
1. Create an instance of LoginDialog by providing a user database and
    an optional main window.
2. Call the `show_login_dialog` function to display the dialog and
    obtain the authenticated user.
"""
import sys
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QMessageBox


class LoginDialog(QDialog):
    """
    LoginDialog class represents a PyQt5-based dialog for user
    authentication and new user creation.

    Args:
    - user_db (UserDatabase): An instance of the UserDatabase class
        providing user authentication
      and creation functionality.
    - main_window (QWidget, optional): An optional reference to the
        main window.

    Attributes:
    - user_db (UserDatabase): The user database for authentication and
        user creation.
    - current_user (str): The authenticated user (None if not authenticated).
    - main_window (QWidget): Reference to the main window (default is None).
    - username_label (QLabel): Label for the username input field.
    - username_input (QLineEdit): Input field for entering the username.
    - password_label (QLabel): Label for the password input field.
    - password_input (QLineEdit): Input field for entering the password
        with echo mode set to Password.
    - login_button (QPushButton): Button to initiate authentication.
    - new_user_button (QPushButton): Button to initiate new user creation.

    Methods:
    - authenticate_user(): Method triggered when the login_button is clicked,
        attempting authentication.
    - create_new_user(): Method triggered when the new_user_button is clicked,
        creating a new user.
    - show_error_message(title: str, message: str): Displays a critical error
        message using QMessageBox.
    - show_info_message(title: str, message: str): Displays an informational
        message using QMessageBox.
    - set_main_window(main_window: QWidget): Sets the main window reference.
    """
    def __init__(self, user_db, main_window=None):
        """
        Initialize the LoginDialog instance.

        Args:
        - user_db (UserDatabase): An instance of the UserDatabase class
            providing user authentication
        and creation functionality.
        - main_window (QWidget, optional): An optional reference to the main
            window.

        Initializes instance attributes, sets up the dialog window with
            labels, input fields,
        buttons, and layout for user authentication and new user creation.

        Note: This method assumes the existence of a UserDatabase class with
            methods `verify_user` and `add_user`
        for user authentication and creation.
        """
        super().__init__()

        self.user_db = user_db
        self.current_user = None
        self.main_window = main_window  # Initialize main_window as None

        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 150)

        self.username_label = ('Username:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.authenticate_user)

        self.new_user_button = QPushButton('Create New User')
        self.new_user_button.clicked.connect(self.create_new_user)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.new_user_button)

        self.setLayout(layout)

    def authenticate_user(self):
        """
        Attempt to authenticate the user using the provided credentials.

        Retrieves the username and password from the input fields, attempts
        to verify
        the user against the user database, and updates the current_user
        attribute if
        authentication is successful. Shows an error message if
        authentication fails.

        Raises:
        - ValueError: If an error occurs during the authentication process.

        Example:
        ```python
        # Assuming login_dialog is an instance of LoginDialog
        login_dialog.authenticate_user()
        ```
        """
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            if self.user_db.verify_user(username, password):
                self.current_user = username
                self.accept()
            else:
                self.show_error_message('Authentication Failed',
                                        'Invalid username or password.')
        except ValueError as err:
            self.show_error_message('Error', str(err))

    def create_new_user(self):
        """
        Create a new user and handle potential errors.

        Retrieves the username and password from the input fields, attempts
        to add
        a new user to the user database, and shows an informational message
        on success.
        If an error occurs during the creation process, a corresponding
        error message is displayed.

        Raises:
        - ValueError: If an error occurs during the user creation process.

        Example:
        ```python
        # Assuming login_dialog is an instance of LoginDialog
        login_dialog.create_new_user()
        ```
        """
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            self.user_db.add_user(username, password)
            self.show_info_message('User Created',
                                   'New user created successfully. \
                                   Please log in.')
        except ValueError as err:
            self.show_error_message('Error', str(err))

    def show_error_message(self, title, message):
        """
        Display a critical error message using QMessageBox.

        Args:
        - title (str): The title of the error message box.
        - message (str): The error message to be displayed.

        Shows a QMessageBox with the specified title, message, and an 'Ok'
        button for the user to acknowledge the error.

        Example:
        ```python
        # Assuming login_dialog is an instance of LoginDialog
        login_dialog.show_error_message('Error', 'An error occurred.
        Please try again.')
        ```
        """
        QMessageBox.critical(self, title, message, QMessageBox.Ok)

    def show_info_message(self, title, message):
        """
        Display an informational message using QMessageBox.

        Args:
        - title (str): The title of the message box.
        - message (str): The informational message to be displayed.

        Shows a QMessageBox with the specified title, message, and an
        'Ok' button for the user to acknowledge the information.

        Example:
        ```python
        # Assuming login_dialog is an instance of LoginDialog
        login_dialog.show_info_message('Information', 'This is an
        informational message.')
        ```
        """
        QMessageBox.information(self, title, message, QMessageBox.Ok)

    def set_main_window(self, main_window):
        """
        Set the reference to the main window.

        Args:
        - main_window (QWidget): The main window reference to be set.

        Sets the main_window attribute to the provided QWidget reference.

        Example:
        ```python
        # Assuming login_dialog is an instance of LoginDialog and
        main_window_instance is a QWidget
        login_dialog.set_main_window(main_window_instance)
        ```
        """
        self.main_window = main_window  # Set main_window


def show_login_dialog(user_db, main_window):
    """
    Attempt to authenticate the user using the provided credentials.

    Retrieves the username and password from the input fields,
    attempts to verify the user against the user database, and
    updates the current_user attribute if authentication is
    successful. Shows an error message if authentication fails.

    Raises:
    - ValueError: If an error occurs during the authentication process.

    Example:
    ```python
    # Assuming login_dialog is an instance of LoginDialog
    login_dialog.authenticate_user()
    ```
    """
    login_dialog = LoginDialog(user_db, main_window)
    result = login_dialog.exec_()

    if result == QDialog.Accepted:
        return login_dialog.current_user
    sys.exit()
