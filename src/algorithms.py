"""Utility algorithms used across OpenTrack."""


def first_unique_index(text):
    """Return the index of the first character that occurs exactly once."""
    if not text:
        return -1

    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1

    for i, ch in enumerate(text):
        if counts[ch] == 1:
            return i

    return -1


def merge_intervals(intervals):
    """Merge overlapping or touching inclusive intervals."""
    if not intervals:
        return []

    normalized = []
    for interval in intervals:
        if len(interval) != 2:
            raise ValueError("interval must contain start and end")
        start, end = interval
        normalized.append((start, end))

    merged = []
    for start, end in sorted(normalized, key=lambda interval: (interval[0], interval[1])):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged
