def format_minimal_seconds(total_seconds: float) -> str:
    """Formats a given duration in seconds in Xm Ys Zms Aus format."""

    # Extract minutes and remaining fractional seconds
    minutes, remainder = divmod(total_seconds, 60)

    # Extract whole seconds
    seconds = int(remainder)
    sub_seconds = remainder - seconds

    # Extract milliseconds and microseconds safely to avoid float rounding errors
    total_microseconds = round(sub_seconds * 1_000_000)
    milliseconds, microseconds = divmod(total_microseconds, 1000)

    parts = []

    # Only add units if they are greater than zero
    if minutes > 0:
        parts.append(f"{int(minutes)}m")

    if seconds > 0:
        parts.append(f"{seconds}s")

    if milliseconds > 0:
        parts.append(f"{milliseconds}ms")

    if microseconds > 0:
        parts.append(f"{microseconds}µs")

    # Fallback if the duration is exactly 0
    if not parts:
        return "0µs"

    return " ".join(parts)
