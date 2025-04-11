"""
    Utility functions for the library.
"""

import pandas as pd
import numpy as np

from enum import Enum
from typing import List, Union

TEXT_COLORING = True
"Global parameter that can turn off coloring of the text."


def set_text_color(value: bool):
    """Sets the text color for colored output.

    Args:
        value (bool): If True, text color is enabled. If False, text color is disabled.
    """
    global TEXT_COLORING
    TEXT_COLORING = value


def merge_intervals(intervals: List[pd.Interval]) -> List[pd.Interval]:
    """Merges a list of pandas Interval objects, combining overlapping and adjacent intervals.

    Args:
        intervals (List[pd.Interval]): A list of pandas Interval objects to be merged.

    Returns:
        List[pd.Interval]: A list of merged pandas Interval objects.
        The function performs the following steps:
        1. Sorts the intervals by their start time.
        2. Iterates through the sorted intervals and merges overlapping or adjacent intervals.
        3. Returns the list of merged intervals.

    Notes:
    - Intervals are considered overlapping if they share any common points.
    - Intervals are considered adjacent if the end of one interval is the start of another.
    - The function handles both open and closed intervals.
    """
    # Step 0: Check if the input is valid
    if not isinstance(intervals, List) or len(intervals) <= 1:
        return intervals

    # Step 1: Sort the intervals by the start time
    intervals.sort(key=lambda x: x.left)

    # Step 2: Initialize the list to hold merged intervals
    merged_intervals: List[pd.Interval] = []

    # Step 3: Iterate through the sorted intervals
    for interval in intervals:
        # If merged_intervals is empty or there is no overlap, append the interval

        if (
            not merged_intervals or
            merged_intervals[-1].right < interval.left or
            # interval is not inside the previous one
            merged_intervals[-1].right != interval.left or
            # interval is not adjacent to the previous one
            (merged_intervals[-1].open_right and interval.open_left)
        ):
            merged_intervals.append(interval)
        else:
            # There is an overlap, so merge the current interval with the last one in merged_intervals
            left = merged_intervals[-1].left
            right = max(merged_intervals[-1].right, interval.right)
            closed = "neither"

            if merged_intervals[-1].closed_left and interval.closed_right:
                closed = "both"
            elif merged_intervals[-1].closed_left:
                closed = "left"
            elif interval.closed_right:
                closed = "right"

            merged_intervals[-1] = pd.Interval(left=left, right=right, closed=closed)
    return merged_intervals


class Colors(Enum):
    "4-bit color codes. For more information see https://en.wikipedia.org/wiki/ANSI_escape_code."
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


def colored(text: str, color: Colors):
    "Returns colored text using ANSI escape codes"
    if not TEXT_COLORING:
        return text
    return f"\x1b[{color.value}m{text}\x1b[0m"


def equidistant_intervals(data: Union[pd.DataFrame, pd.Series], prefix: str = "", step: int = 1):
    """Converts continuous data into equidistant intervals.
    For each column make equidistant intervals and assign row to correct interval."""
    result = pd.DataFrame()
    if isinstance(data, pd.Series):
        data = data.to_frame()
    for column in data.columns:
        seq = np.arange(min(data[column]), max(data[column]) + step, step)
        result[prefix + column] = pd.cut(data[column], seq, include_lowest=True)
    return result


def _unpack(x):
    """Unpacks a list with a single element into the element itself.

    Why is this useful:
    - Coefficient generators return list of tuples, if length is 1, we unpack it.
    - Tuples are converted to lists.
    """
    if type(x) not in [tuple, list]:
        return x
    return list(x) if len(x) > 1 else x[0]
