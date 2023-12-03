"""
UserDatabase Module

This module provides a simple SQLite-based user database functionality.
It includes a UserDatabase class that allows for the creation of a user
database, addition of users with securely hashed passwords, verification
of users, and closing of the database connection.

Usage:
    # Example usage:
    user_db = UserDatabase()

    # Add a user
    user_db.add_user('john_doe', 'password123')

    try:
        # Attempt to add a user with an existing username
        user_db.add_user('john_doe', 'another_password')
    except ValueError as e:
        print(f'Error: {e}')

    try:
        # Attempt to verify user with wrong password
        user_db.verify_user('john_doe', 'wrong_password')
    except ValueError as e:
        print(f'Error: {e}')

    try:
        # Attempt to verify a user that does not exist
        user_db.verify_user('nonexistent_user', 'password')
    except ValueError as e:
        print(f'Error: {e}')

    # Close the database connection when done
    user_db.close_connection()

Note:
    The passwords are securely hashed using PBKDF2-HMAC-SHA256 with a
    randomly generated salt for each user. This enhances the security
    of stored passwords by preventing common attacks like rainbow
    table attacks.

    It is recommended to customize the database name when creating an
    instance of the UserDatabase class to avoid potential conflicts
    with other databases in the same directory.
"""

import sqlite3
import os
from hashlib import pbkdf2_hmac
from secrets import token_bytes


class UserDatabase:
    """
    UserDatabase Class

    This class provides a simple SQLite-based user database functionality.
    It includes methods for creating the database, adding users with securely
    hashed passwords, verifying users, and closing the database connection.

    Usage:
        # Example usage:
        user_db = UserDatabase()

        # Add a user
        user_db.add_user('john_doe', 'password123')

        try:
            # Attempt to add a user with an existing username
            user_db.add_user('john_doe', 'another_password')
        except ValueError as e:
            print(f'Error: {e}')

        try:
            # Attempt to verify user with wrong password
            user_db.verify_user('john_doe', 'wrong_password')
        except ValueError as e:
            print(f'Error: {e}')

        try:
            # Attempt to verify a user that does not exist
            user_db.verify_user('nonexistent_user', 'password')
        except ValueError as e:
            print(f'Error: {e}')

        # Close the database connection when done
        user_db.close_connection()

    Methods:
        __init__(self, db_name='user_database.db'):
            Initializes the UserDatabase object and establishes a connection
            to the SQLite database. If the database does not exist, it creates
            the necessary table.

        create_table(self):
            Creates the 'Users' table if it does not exist. The table schema
            includes fields for the username, salt, and hashed password.

        add_user(self, username, password):
            Adds a new user to the database with the provided username and
            securely hashed password. Raises a ValueError if the username
            already exists.

        _hash_password(self, password, salt):
            Hashes the provided password using PBKDF2-HMAC-SHA256 with the
            given salt. This private method is used internally for securely
            storing passwords.

        verify_user(self, username, password):
            Verifies the provided username and password combination against
            the stored credentials. Raises a ValueError if the username or
            password is incorrect.

        _user_exists(self, username):
            Checks if a user with the given username already exists in the
            database.

        close_connection(self):
            Closes the SQLite database connection.

    Note:
        The passwords are securely hashed using PBKDF2-HMAC-SHA256 with a
        randomly generated salt for each user. This enhances the security
        of stored passwords by preventing common attacks like rainbow
        table attacks.

        It is recommended to customize the database name when creating an
        instance of the UserDatabase class to avoid potential conflicts
        with other databases in the same directory.
    """

    def __init__(self, db_name='user_database.db'):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the database path relative to the script
        # directory and with the specified db_name
        db_path = os.path.join(script_dir, db_name)

        # Get the absolute path of the constructed db_path
        abs_db_path = os.path.abspath(db_path)
        self.connection = sqlite3.connect(abs_db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """
    create_table method

    Creates the 'Users' table in the SQLite database if it does not already exist.
    The table schema includes fields for the username, salt, and hashed password.

    Parameters:
        self: UserDatabase
            An instance of the UserDatabase class.

    Returns:
        None

    Note:
        This method is called during the initialization of the UserDatabase
        object to ensure that the required 'Users' table is present in the
        database. If the table already exists, no action is taken.
    """

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                Username varchar(255) PRIMARY KEY,
                Salt BINARY(16),
                Hash BINARY(16)
            )
        ''')
        self.connection.commit()

    def add_user(self, username, password):
        """
    add_user method

    Adds a new user to the 'Users' table with the provided username and securely
    hashed password. Raises a ValueError if the username already exists.

    Parameters:
        self: UserDatabase
            An instance of the UserDatabase class.
        username: str
            The username to be added.
        password: str
            The plaintext password for the user.

    Returns:
        None

    Note:
        The method generates a random salt using the `token_bytes` function and
        then securely hashes the provided password using the `_hash_password`
        method. The hashed password, along with the username and salt, is then
        inserted into the 'Users' table. The database connection is committed
        to persist the changes.
    """

        # Check if the username is already in use
        if self._user_exists(username):
            raise ValueError('Username already in use. \
                             Choose a different username.')

        salt = token_bytes(16)
        hashed_password = self._hash_password(password, salt)
        self.cursor.execute('INSERT INTO Users (Username, Salt, Hash) \
                            VALUES (?, ?, ?)',
                            (username, salt, hashed_password))
        self.connection.commit()

    def _hash_password(self, password, salt):
        iterations = 100000
        key_length = 16  # 128 bits
        hash_function = 'sha256'
        hashed_password = pbkdf2_hmac(hash_function,
                                      password.encode('utf-8'),
                                      salt, iterations, key_length)
        return hashed_password

    def verify_user(self, username, password):
        """
    verify_user method

    Verifies the provided username and password combination against the stored
    credentials in the 'Users' table. Raises a ValueError if the username or
    password is incorrect.

    Parameters:
        self: UserDatabase
            An instance of the UserDatabase class.
        username: str
            The username to be verified.
        password: str
            The password to be verified.

    Returns:
        bool
            True if the provided username and password combination is correct,
            False otherwise.

    Note:
        The method retrieves user data from the 'Users' table based on the
        provided username. It then hashes the provided password using the
        stored salt and compares it with the stored hash. If the provided
        password is correct, the method returns True; otherwise, it raises
        a ValueError with an appropriate error message.
    """

        self.cursor.execute('SELECT * FROM Users WHERE Username=?',
                            (username,))
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
        self.cursor.execute('SELECT * FROM Users WHERE Username=?',
                            (username,))
        return self.cursor.fetchone() is not None

    def close_connection(self):
        """
    close_connection method

    Closes the SQLite database connection.

    Parameters:
        self: UserDatabase
            An instance of the UserDatabase class.

    Returns:
        None

    Note:
        This method is used to gracefully close the database connection when
        it is no longer needed. It is recommended to call this method after
        completing all database operations to free up resources.
    """

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
