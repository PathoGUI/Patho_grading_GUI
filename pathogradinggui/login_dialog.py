# login_dialog.py
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication, QMessageBox
import sys

class LoginDialog(QDialog):
    def __init__(self, user_db, main_window=None):
        super().__init__()

        self.user_db = user_db
        self.current_user = None
        self.main_window = main_window  # Initialize main_window as None

        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 150)

        self.username_label = QLabel('Username:')
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
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            if self.user_db.verify_user(username, password):
                self.current_user = username
                self.accept()
            else:
                self.show_error_message('Authentication Failed', 'Invalid username or password.')
        except ValueError as e:
            self.show_error_message('Error', str(e))

    def create_new_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            self.user_db.add_user(username, password)
            self.show_info_message('User Created', 'New user created successfully. Please log in.')
        except ValueError as e:
            self.show_error_message('Error', str(e))

    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message, QMessageBox.Ok)

    def show_info_message(self, title, message):
        QMessageBox.information(self, title, message, QMessageBox.Ok)

    def set_main_window(self, main_window):
        self.main_window = main_window  # Set main_window


def show_login_dialog(user_db, main_window):
    login_dialog = LoginDialog(user_db, main_window)
    result = login_dialog.exec_()

    if result == QDialog.Accepted:
        return login_dialog.current_user
    else:
        sys.exit()
