
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
    """Merge overlapping or touching intervals."""
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda interval: interval[0])
    merged = [list(sorted_intervals[0])]

    for start, end in sorted_intervals[1:]:
        last = merged[-1]

        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return merged
