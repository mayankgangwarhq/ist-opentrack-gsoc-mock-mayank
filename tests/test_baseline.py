
"""JSON file persistence for OpenTrack."""

import json
import os


class JsonStorage:
    """Persists issues and the next available ID to a JSON file."""

    def __init__(self, path):
        self.path = path
        self.next_id = 1

    def load(self):
        """Load issues and preserve ID continuity."""
        if not os.path.exists(self.path):
            self.next_id = 1
            return {}

        with open(self.path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        issues = {
            int(k): v for k, v in raw.get("issues", {}).items()
        }

        # Support existing files that don't contain next_id.
        minimum_next_id = max(issues, default=0) + 1
        self.next_id = max(
            raw.get("next_id", minimum_next_id),
            minimum_next_id,
        )

        return issues

    def save(self, issues, next_id=None):
        """Write issues and the next available ID to disk."""
        if next_id is not None:
            self.next_id = max(next_id, max(issues, default=0) + 1)
        else:
            self.next_id = max(
                self.next_id,
                max(issues, default=0) + 1,
            )

        payload = {
            "issues": {str(k): v for k, v in issues.items()},
            "next_id": self.next_id,
        }

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
