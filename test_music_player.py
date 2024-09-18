import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from tkinter import Tk, messagebox
from main import SignInSignUp, is_password_valid  # Replace 'your_module' with the actual module name

class TestSignInSignUp(unittest.TestCase):

    @patch('main.sqlite3.connect')
    def setUp(self, mock_connect):
        self.mock_conn = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.sign_in_sign_up = SignInSignUp()
        self.sign_in_sign_up.username_entry = MagicMock()
        self.sign_in_sign_up.password_entry = MagicMock()

    def test_sign_in_success(self):
        # Set up mocks
        self.sign_in_sign_up.username_entry.get.return_value = 'testuser'
        self.sign_in_sign_up.password_entry.get.return_value = 'testpass'
        self.mock_conn.execute.return_value.fetchone.return_value = ('testuser', 'testpass')
        
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.sign_in_sign_up.sign_in()
            mock_showinfo.assert_called_once_with("Success", "Login successful!")

    def test_sign_in_failure(self):
        # Set up mocks
        self.sign_in_sign_up.username_entry.get.return_value = 'testuser'
        self.sign_in_sign_up.password_entry.get.return_value = 'wrongpass'
        self.mock_conn.execute.return_value.fetchone.return_value = None
        
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.sign_in_sign_up.sign_in()
            mock_showerror.assert_called_once_with("Error", "Invalid username or password")

    def test_sign_up_success(self):
        # Set up mocks
        self.sign_in_sign_up.username_entry.get.return_value = 'newuser'
        self.sign_in_sign_up.password_entry.get.return_value = 'Valid1Password@'
        self.mock_conn.execute.return_value = None
        
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.sign_in_sign_up.sign_up()
            mock_showinfo.assert_called_once_with("Success", "Sign-up successful! You can now sign in.")

    def test_sign_up_failure_username_exists(self):
        # Set up mocks
        self.sign_in_sign_up.username_entry.get.return_value = 'existinguser'
        self.sign_in_sign_up.password_entry.get.return_value = 'Valid1Password@'
        self.mock_conn.execute.side_effect = sqlite3.IntegrityError
        
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.sign_in_sign_up.sign_up()
            mock_showerror.assert_called_once_with("Error", "Username already exists")

    def test_password_validation(self):
        self.assertTrue(is_password_valid('Valid1Password@'))
        self.assertFalse(is_password_valid('short'))
        self.assertFalse(is_password_valid('NoNumber!'))
        self.assertFalse(is_password_valid('NoSpecial123'))

if __name__ == '__main__':
    unittest.main()
