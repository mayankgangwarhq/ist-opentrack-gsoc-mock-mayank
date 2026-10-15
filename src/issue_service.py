"""Core issue management service for OpenTrack."""

from . import validators


class IssueNotFound(KeyError):
    """Raised when an issue id does not exist."""


class IssueService:
    def __init__(self, storage):
        self.storage = storage
        self.issues = self.storage.load()

    def _next_id(self):
        if not self.issues:
            return 1
        return max(self.issues) + 1

    def create(self, data):
        """Create a new issue and return it."""
        normalized = validators.validate_new_issue(data)
        issue_id = self._next_id()
        issue = {"id": issue_id}
        issue.update(normalized)
        self.issues[issue_id] = issue
        self.storage.save(self.issues)
        return dict(issue)

    def get(self, issue_id):
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")
        return dict(self.issues[issue_id])

    def list_all(self):
        return [dict(self.issues[k]) for k in sorted(self.issues)]

    def update(self, issue_id, changes):
        """Partially update an issue, preserving omitted fields."""
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")

        normalized = validators.validate_issue_changes(changes)

        merged = dict(self.issues[issue_id])
        merged.update(normalized)

        self.issues[issue_id] = merged
        self.storage.save(self.issues)

        return dict(merged)

    def delete(self, issue_id):
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")
        del self.issues[issue_id]
        self.storage.save(self.issues)

    def find(self, status=None, priority=None, title_contains=None):
        """Filter issues by status, priority, and title text."""
        if status is not None:
            status = validators.validate_status(status)
        if priority is not None:
            priority = validators.validate_priority(priority)
        if title_contains is not None and not isinstance(title_contains, str):
            raise validators.ValidationError("title filter must be a string")

        needle = title_contains.lower() if title_contains is not None else None
        matches = []
        for issue in self.list_all():
            if status is not None and issue["status"] != status:
                continue
            if priority is not None and issue["priority"] != priority:
                continue
            if needle is not None and needle not in issue["title"].lower():
                continue
            matches.append(issue)
        return matches
