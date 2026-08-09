import os
import tempfile
import unittest

from app import create_app, init_db


class TaskManagerAppTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp_dir.name, "tasks.sqlite3")
        self.app = create_app({"TESTING": True, "DATABASE": self.db_path})
        self.client = self.app.test_client()

        with self.app.app_context():
            init_db()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("TaskFlow", response.get_data(as_text=True))

    def test_can_create_task(self):
        response = self.client.post(
            "/tasks",
            data={
                "title": "Preparar entrevista",
                "description": "Repasar proyectos y preguntas técnicas",
                "priority": "alta",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Preparar entrevista", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
