import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.database import get_supabase
from app.main import app


class AppStartupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_root_endpoint(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"message": "API funcionando correctamente"},
        )

    def test_missing_supabase_variables_do_not_break_app_startup(self) -> None:
        get_supabase.cache_clear()

        with patch.dict(os.environ, {}, clear=True):
            health_response = self.client.get("/health")

            self.assertEqual(health_response.status_code, 200)
            with self.assertRaisesRegex(RuntimeError, "SUPABASE_URL"):
                get_supabase()

        get_supabase.cache_clear()


if __name__ == "__main__":
    unittest.main()
