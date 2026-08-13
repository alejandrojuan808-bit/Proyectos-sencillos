import os
import tempfile
import unittest
from pathlib import Path

from app.auth import InvalidCredentialsError, UserAlreadyExistsError, login_user, register_user
from app.storage import DATA_FILE


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_data_file = DATA_FILE
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("{}", encoding="utf-8")

    def tearDown(self):
        if DATA_FILE.exists():
            DATA_FILE.unlink()

    def test_register_user_success(self):
        response = register_user("ana", "12345")
        self.assertEqual(response["username"], "ana")
        self.assertIn("registrado", response["message"].lower())

    def test_register_duplicate_user_raises(self):
        register_user("ana", "12345")
        with self.assertRaises(UserAlreadyExistsError):
            register_user("ana", "45678")

    def test_login_user_success(self):
        register_user("ana", "12345")
        response = login_user("ana", "12345")
        self.assertEqual(response["username"], "ana")

    def test_login_user_wrong_password_raises(self):
        register_user("ana", "12345")
        with self.assertRaises(InvalidCredentialsError):
            login_user("ana", "wrong")


if __name__ == "__main__":
    unittest.main()
