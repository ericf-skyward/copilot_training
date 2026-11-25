import unittest
from unittest.mock import patch

import httpx

from src.app import activities, app


class UnregisterTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.activities_patch = patch.dict(activities, {
            "Test Activity": {"participants": ["student@example.com", "other@example.com",
                                               "student@example.com"]}
        })
        self.activities_patch.start()
        self.addCleanup(self.activities_patch.stop)
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        )
        self.addAsyncCleanup(self.client.aclose)

    async def test_unregister_removes_all_matching_entries_only(self):
        response = await self.client.delete(
            "/activities/Test%20Activity/signup", params={"email": "student@example.com"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(activities["Test Activity"]["participants"], ["other@example.com"])

    async def test_missing_activity_or_participant_returns_404(self):
        for activity, email in [
            ("Missing", "student@example.com"),
            ("Test Activity", "missing@example.com"),
        ]:
            with self.subTest(activity=activity, email=email):
                response = await self.client.delete(
                    f"/activities/{activity}/signup", params={"email": email}
                )
                self.assertEqual(response.status_code, 404)
        self.assertEqual(len(activities["Test Activity"]["participants"]), 3)


if __name__ == "__main__":
    unittest.main()
