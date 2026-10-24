
import re
from collections import Counter


def analyze_logs(log_text):
    """
    Analyze application logs and return basic statistics.
    """

    lines = [
        line.strip()
        for line in log_text.splitlines()
        if line.strip()
    ]

    level_counts = Counter()
    error_messages = []

    for line in lines:
        match = re.search(
            r"\b(ERROR|WARN(?:ING)?|INFO|DEBUG)\b",
            line,
            re.IGNORECASE
        )

        if not match:
            continue

        level = match.group(1).upper()

        # Treat WARNING and WARN as the same category.
        if level == "WARNING":
            level = "WARN"

        level_counts[level] += 1

        if level == "ERROR":
            # Remove the timestamp and severity to help
            # identify repeated error patterns.
            message = re.sub(
                r"^\s*\d{4}-\d{2}-\d{2}\s+"
                r"\d{2}:\d{2}:\d{2}\s+",
                "",
                line
            )

            message = re.sub(
                r"^\s*ERROR\s*[-:]?\s*",
                "",
                message,
                flags=re.IGNORECASE
            )

            error_messages.append(message)

    repeated_errors = Counter(error_messages)

    return {
        "total_lines": len(lines),
        "error_count": level_counts["ERROR"],
        "warning_count": level_counts["WARN"],
        "info_count": level_counts["INFO"],
        "debug_count": level_counts["DEBUG"],
        "error_messages": error_messages,
        "repeated_errors": {
            message: count
            for message, count in repeated_errors.items()
            if count > 1
        },
    }
