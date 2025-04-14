"""
Included generic parser functions which can be used by client developer commands.
"""


def string_parser(args: str) -> str:
    """
    Returns the stripped argument string without further modification.
    """
    return args.strip()


def no_arguments(args: str) -> None:
    """
    Use when a command accepts no arguments.
    """
    if args.strip():
        raise ParseError("This command takes no arguments.")
    return None


def pull_segment(args: str) -> tuple[str, str]:
    """
    Splits a string once and returns the first segment as well as the remainder.
    """
    result = args.split(maxsplit=1)
    segment = result.pop(0)
    remainder = result[0] if result else ""
    return segment, remainder


class ParseError(Exception):
    """
    Throw when there is a parsing error.
    """
