import sqlite3
import os
from hashlib import pbkdf2_hmac
from secrets import token_bytes

class UserDatabase:
    def __init__(self, db_name='user_database.db'):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the database path relative to the script directory and with the specified db_name
        db_path = os.path.join(script_dir, db_name)
        
        # Get the absolute path of the constructed db_path
        abs_db_path = os.path.abspath(db_path)
        self.connection = sqlite3.connect(abs_db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                Username varchar(255) PRIMARY KEY,
                Salt BINARY(16),
                Hash BINARY(16)
            )
        ''')
        self.connection.commit()

    def add_user(self, username, password):
        # Check if the username is already in use
        if self._user_exists(username):
            raise ValueError('Username already in use. Choose a different username.')

        salt = token_bytes(16)
        hashed_password = self._hash_password(password, salt)
        self.cursor.execute('INSERT INTO Users (Username, Salt, Hash) VALUES (?, ?, ?)', (username, salt, hashed_password))
        self.connection.commit()

    def _hash_password(self, password, salt):
        iterations = 100000
        key_length = 16  # 128 bits
        hash_function = 'sha256'
        hashed_password = pbkdf2_hmac(hash_function, password.encode('utf-8'), salt, iterations, key_length)
        return hashed_password

    def verify_user(self, username, password):
        self.cursor.execute('SELECT * FROM Users WHERE Username=?', (username,))
        user_data = self.cursor.fetchone()
        
        if user_data:
            stored_salt = user_data[1]
            stored_hash = user_data[2]
            hashed_password = self._hash_password(password, stored_salt)

            # Check if the provided password is correct
            if hashed_password == stored_hash:
                return True
            else:
                raise ValueError('Wrong password. Please try again.')
        else:
            raise ValueError('User does not exist. Please check the username.')

    def _user_exists(self, username):
        self.cursor.execute('SELECT * FROM Users WHERE Username=?', (username,))
        return self.cursor.fetchone() is not None

    def close_connection(self):
        self.connection.close()

# # Example usage:
# user_db = UserDatabase()

# # Add a user
# user_db.add_user('john_doe', 'password123')

# try:
#     # Attempt to add a user with an existing username
#     user_db.add_user('john_doe', 'another_password')
# except ValueError as e:
#     print(f'Error: {e}')

# try:
#     # Attempt to verify user with wrong password
#     user_db.verify_user('john_doe', 'wrong_password')
# except ValueError as e:
#     print(f'Error: {e}')

# try:
#     # Attempt to verify a user that does not exist
#     user_db.verify_user('nonexistent_user', 'password')
# except ValueError as e:
#     print(f'Error: {e}')

# # Close the database connection when done
# user_db.close_connection()
