"""
Helper utilities for application building.
"""

from collections.abc import Iterable

from pax25.services.connection.connection import Connection


def send_message(
    connection: Connection, message: str, append_newline: bool = True
) -> None:
    """
    Send a message string to a particular connection.
    """
    if append_newline:
        message += "\r"
    connection.send_bytes(message.encode("utf-8"))


def build_columns(
    entries_list: Iterable[str],
    num_columns: int = 6,
    column_width: int = 10,
) -> list[str]:
    """
    Build lines of help topic columns. Set num_columns to the number of columns to sort
    the entries into.
    """
    topic_sets = []
    current_set = []
    for entry in entries_list:
        current_set.append(entry)
        if len(current_set) == num_columns:
            topic_sets.append(current_set)
            current_set = []
    if current_set:
        topic_sets.append(current_set)
    # This might truncate some commands, but since there's autocomplete, it's
    # unlikely to matter.
    lines = []
    for topic_set in topic_sets:
        string = ""
        for entry in topic_set:
            string += entry[:column_width].ljust(column_width)
        string = string.rstrip()
        lines.append(string)
    return lines
