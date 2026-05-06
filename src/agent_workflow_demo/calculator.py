"""Small calculator module used by the debug demo."""


def add(left: float, right: float) -> float:
    """Return left plus right.

    The live debug demo intentionally changes this line to subtraction via
    scripts/reset-demo.sh. The fix should be minimal: restore addition.
    """
    return left + right


def divide(left: float, right: float) -> float:
    """Return left divided by right."""
    if right == 0:
        raise ZeroDivisionError("division by zero")
    return left / right


def format_number(value: float) -> str:
    """Format numbers for stable CLI output."""
    return f"{value:g}"
