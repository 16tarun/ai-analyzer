
from ai_analyzer import analyze_with_ai


def test_missing_api_key_uses_safe_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = analyze_with_ai(
        log_text="Example application log",
        log_results={
            "total_lines": 1,
            "error_count": 0,
            "warning_count": 0,
            "info_count": 1,
        },
        incident={
            "severity": "Low",
            "score": 0,
            "rationale": "No major indicators detected.",
            "evidence": [],
            "hypotheses": [],
        },
    )

    assert result["ok"] is False
    assert result["analysis"] == ""
    assert "OPENAI_API_KEY" in result["error"]
