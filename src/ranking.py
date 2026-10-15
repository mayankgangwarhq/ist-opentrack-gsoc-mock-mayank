"""Ranking of open issues for the triage dashboard."""


_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def rank_open_issues(issues, limit):
    """Return up to ``limit`` issue ids for triage.

    Only open issues are considered. Priority order is high, medium, low,
    and ids are sorted ascending within the same priority. The input list is
    not modified.
    """
    candidates = [issue for issue in issues if issue.get("status") == "open"]
    ranked = sorted(
        candidates,
        key=lambda issue: (
            _PRIORITY_ORDER.get(issue.get("priority", "medium"), 99),
            issue.get("id", 0),
        ),
    )

    if limit is None:
        return [issue["id"] for issue in ranked]
    if limit <= 0:
        return []
    return [issue["id"] for issue in ranked[:limit]]
