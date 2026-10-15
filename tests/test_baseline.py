"""Public starter tests and regression tests for OpenTrack."""

import unittest

from src.issue_service import IssueNotFound, IssueService
from src.validators import ValidationError

class MemoryStorage:
    """In-memory storage for tests."""

    def __init__(self):
        self.data = {}

    def load(self):
        return dict(self.data)

    def save(self, issues):
        self.data = dict(issues)

class TestBaseline(unittest.TestCase):
    def setUp(self):
        self.service = IssueService(MemoryStorage())
    def test_create_assigns_id_and_defaults(self):
        issue = self.service.create({"title": "First bug"})
        self.assertEqual(issue["id"], 1)
        self.assertEqual(issue["status"], "open")
        self.assertEqual(issue["priority"], "medium")

    def test_ids_increase(self):
        a = self.service.create({"title": "Issue A"})
        b = self.service.create({"title": "Issue B"})
        self.assertEqual((a["id"], b["id"]), (1, 2))

    def test_get_returns_created_issue(self):
        created = self.service.create({
            "title": "Readable title",
            "priority": "high",
        })
        fetched = self.service.get(created["id"])
        self.assertEqual(fetched["title"], "Readable title")
        self.assertEqual(fetched["priority"], "high")

    def test_get_missing_raises(self):
        with self.assertRaises(IssueNotFound):
            self.service.get(42)

    def test_list_sorted_by_id(self):
        for name in ("one", "two", "three"):
            self.service.create({"title": f"issue {name}"})
        ids = [i["id"] for i in self.service.list_all()]
        self.assertEqual(ids, [1, 2, 3])

    def test_invalid_title_rejected(self):
        with self.assertRaises(ValidationError):
            self.service.create({"title": "ab"})

    def test_invalid_priority_rejected(self):
        with self.assertRaises(ValidationError):
            self.service.create({
                "title": "valid title",
                "priority": "urgent",
            })

    def test_delete_removes_issue(self):
        issue = self.service.create({"title": "to be removed"})
        self.service.delete(issue["id"])
        with self.assertRaises(IssueNotFound):
            self.service.get(issue["id"])

    def test_update_status_preserves_title_and_priority(self):
        issue = self.service.create({
            "title": "Original issue",
            "priority": "high",
        })
        updated = self.service.update(
            issue["id"], {"status": "closed"}
        )
        self.assertEqual(updated["title"], "Original issue")
        self.assertEqual(updated["priority"], "high")
        self.assertEqual(updated["status"], "closed")

    def test_update_priority_preserves_other_fields(self):
        issue = self.service.create({
            "title": "Original issue",
            "priority": "low",
        })
        updated = self.service.update(
            issue["id"], {"priority": "high"}
        )
        self.assertEqual(updated["title"], "Original issue")
        self.assertEqual(updated["priority"], "high")
        self.assertEqual(updated["status"], "open")

    def test_invalid_partial_update_preserves_issue(self):
        issue = self.service.create({"title": "Original issue"})
        with self.assertRaises(ValidationError):
            self.service.update(
                issue["id"], {"status": "invalid"}
            )
        self.assertEqual(self.service.get(issue["id"]), issue)

    def test_invalid_title_in_partial_update_is_rejected(self):
        issue = self.service.create({"title": "Original issue"})
        with self.assertRaises(ValidationError):
            self.service.update(
                issue["id"], {"title": "ab"}
            )
        self.assertEqual(self.service.get(issue["id"]), issue)

    def test_empty_partial_update_is_rejected(self):
        issue = self.service.create({"title": "Original issue"})
        with self.assertRaises(ValidationError):
            self.service.update(issue["id"], {})
        self.assertEqual(self.service.get(issue["id"]), issue)

    def test_unknown_partial_update_field_is_rejected(self):
        issue = self.service.create({"title": "Original issue"})
        with self.assertRaises(ValidationError):
            self.service.update(
                issue["id"], {"owner": "Mayank"}
            )
        self.assertEqual(self.service.get(issue["id"]), issue)


if __name__ == "__main__":
    unittest.main()
