import ast
from pathlib import Path
import unittest


DATABASE_PATH = Path(__file__).resolve().parents[1] / "src" / "backend" / "database.py"


def load_initial_activities():
    module = ast.parse(DATABASE_PATH.read_text())

    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue

        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "initial_activities":
                return ast.literal_eval(node.value)

    raise AssertionError("initial_activities definition not found")


class InitialActivitiesTest(unittest.TestCase):
    def test_manga_maniacs_is_seeded(self):
        activities = load_initial_activities()

        self.assertIn("Manga Maniacs", activities)
        activity = activities["Manga Maniacs"]

        self.assertEqual(
            activity["description"],
            "Dive into epic adventures, unforgettable heroes, and dramatic rivalries from the world of Japanese manga (graphic novels).",
        )
        self.assertEqual(activity["schedule"], "Tuesdays, 7:00 PM - 8:00 PM")
        self.assertEqual(
            activity["schedule_details"],
            {
                "days": ["Tuesday"],
                "start_time": "19:00",
                "end_time": "20:00",
            },
        )
        self.assertEqual(activity["max_participants"], 15)
        self.assertEqual(activity["participants"], [])

    def test_difficulty_is_optional_and_uses_supported_values(self):
        activities = load_initial_activities()
        allowed_levels = {"Beginner", "Intermediate", "Advanced"}

        activities_with_difficulty = [
            details
            for details in activities.values()
            if "difficulty" in details
        ]
        activities_without_difficulty = [
            details
            for details in activities.values()
            if "difficulty" not in details
        ]

        self.assertGreater(len(activities_with_difficulty), 0)
        self.assertGreater(len(activities_without_difficulty), 0)

        for activity in activities_with_difficulty:
            self.assertIn(activity["difficulty"], allowed_levels)


if __name__ == "__main__":
    unittest.main()
