from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication, QMessageBox
import sys
sys.path.append("./users")
from users.User import UserDatabase
from GUI_pyqt5 import MainWindow
from login_dialog import show_login_dialog

if __name__ == '__main__':
    app = QApplication([])

    # Initialize the user database
    user_db = UserDatabase()
    
    # Show the login dialog
    current_user = show_login_dialog(user_db)

    # Now, only if authentication is successful, create and show the main window
    if current_user:
        w = MainWindow(current_user)
        show_login_dialog(user_db, w)
        sys.exit(app.exec_())
