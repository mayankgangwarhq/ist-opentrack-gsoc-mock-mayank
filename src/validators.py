"""Validation rules for OpenTrack issues."""

VALID_PRIORITIES = ("low", "medium", "high")
VALID_STATUSES = ("open", "in_progress", "closed")

TITLE_MIN = 3
TITLE_MAX = 80


class ValidationError(ValueError):
    """Raised when user-supplied issue data is invalid."""


def validate_title(title):
    if not isinstance(title, str):
        raise ValidationError("title must be a string")
    title = title.strip()
    if not (TITLE_MIN <= len(title) <= TITLE_MAX):
        raise ValidationError(
            f"title must be between {TITLE_MIN} and {TITLE_MAX} characters after trimming"
        )
    return title


def validate_priority(priority):
    if priority not in VALID_PRIORITIES:
        raise ValidationError(f"priority must be one of {VALID_PRIORITIES}")
    return priority


def validate_status(status):
    if status not in VALID_STATUSES:
        raise ValidationError(f"status must be one of {VALID_STATUSES}")
    return status


def validate_new_issue(data):
    """Validate payload for creating a new issue. Returns a normalized dict."""
    if not isinstance(data, dict):
        raise ValidationError("issue payload must be a dict")
    title = validate_title(data.get("title"))
    priority = validate_priority(data.get("priority", "medium"))
    status = validate_status(data.get("status", "open"))
    return {"title": title, "priority": priority, "status": status}


def validate_issue_changes(changes):
    """Validate only fields supplied for a partial update."""
    if not isinstance(changes, dict):
        raise ValidationError("update payload must be a dict")

    if not changes:
        raise ValidationError("update payload must contain at least one field")

    allowed_fields = {"title", "priority", "status"}
    unknown_fields = set(changes) - allowed_fields

    if unknown_fields:
        raise ValidationError(
            f"unknown update fields: {sorted(unknown_fields)}"
        )

    normalized = {}

    if "title" in changes:
        normalized["title"] = validate_title(changes["title"])

    if "priority" in changes:
        normalized["priority"] = validate_priority(changes["priority"])

    if "status" in changes:
        normalized["status"] = validate_status(changes["status"])

    return normalized
