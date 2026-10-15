"""Regression tests for the OpenTrack issue tracker."""

import unittest

from src.algorithms import merge_intervals
from src.issue_service import IssueService
from src.ranking import rank_open_issues


class MemoryStorage:
    def __init__(self):
        self.data = {}

    def load(self):
        return dict(self.data)

    def save(self, issues):
        self.data = dict(issues)


class TestRegressions(unittest.TestCase):
    def test_rank_open_issues_orders_by_priority_and_preserves_input(self):
        issues = [
            {"id": 1, "status": "closed", "priority": "high"},
            {"id": 2, "status": "open", "priority": "low"},
            {"id": 3, "status": "open", "priority": "high"},
            {"id": 4, "status": "open", "priority": "medium"},
            {"id": 5, "status": "open", "priority": "high"},
        ]
        original = [dict(issue) for issue in issues]

        self.assertEqual(rank_open_issues(issues, 3), [3, 5, 4])
        self.assertEqual(issues, original)

    def test_find_filters_by_status_priority_and_title(self):
        service = IssueService(MemoryStorage())
        service.create({"title": "Fix login flow", "priority": "high"})
        service.create({"title": "Improve dashboard", "priority": "medium", "status": "in_progress"})
        service.create({"title": "Clear cache", "priority": "high", "status": "closed"})

        matches = service.find(status="open", priority="high")
        self.assertEqual([issue["title"] for issue in matches], ["Fix login flow"])

        title_match = service.find(title_contains="dash")
        self.assertEqual([issue["title"] for issue in title_match], ["Improve dashboard"])

    def test_merge_intervals_handles_touching_ranges(self):
        self.assertEqual(
            merge_intervals([[1, 3], [2, 5], [8, 9]]),
            [[1, 5], [8, 9]],
        )


if __name__ == "__main__":
    unittest.main()
