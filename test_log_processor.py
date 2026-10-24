
from log_processor import analyze_logs


def test_counts_log_levels():
    logs = """
    2026-10-23 10:00:00 ERROR Payment failed
    2026-10-23 10:00:01 WARN Retry requested
    2026-10-23 10:00:02 INFO Request received
    2026-10-23 10:00:03 DEBUG Checking status
    """

    result = analyze_logs(logs)

    assert result["total_lines"] == 4
    assert result["error_count"] == 1
    assert result["warning_count"] == 1
    assert result["info_count"] == 1
    assert result["debug_count"] == 1


def test_repeated_errors_are_detected():
    logs = """
    2026-10-23 10:00:00 ERROR Database connection failed
    2026-10-23 10:00:01 ERROR Database connection failed
    """

    result = analyze_logs(logs)

    assert result["error_count"] == 2
    assert len(result["repeated_errors"]) == 1
    assert list(result["repeated_errors"].values()) == [2]


def test_empty_logs():
    result = analyze_logs("  \n  ")

    assert result["total_lines"] == 0
    assert result["error_count"] == 0
    assert result["warning_count"] == 0
    assert result["error_messages"] == []
    assert result["repeated_errors"] == {}


def test_unknown_format_does_not_crash():
    result = analyze_logs(
        "This is a log line with an unfamiliar format."
    )

    assert result["total_lines"] == 1
    assert result["error_count"] == 0
