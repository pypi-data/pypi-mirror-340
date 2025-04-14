from typing import Any, NewType, Sequence


class _Auto:
    """
    Sentinel value indicating an automatic default will be used.
    """

    def __bool__(self):
        # Allow `Auto` to be used like `None` or `False` in boolean expressions
        return False


Auto: Any = _Auto()
Volumes = NewType("Volumes", int)  # Volumes of steel or iron (unit: ttpa)
Year = NewType("Year", int)
Years = Sequence[Year]
