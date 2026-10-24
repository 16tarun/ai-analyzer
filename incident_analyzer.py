
import re


def analyze_incident(log_text, log_results):
    """
    Assess incident severity and produce evidence-based hypotheses.
    This is a rule-based estimate, not a confirmed diagnosis.
    """

    text = log_text.lower()
    evidence = []
    hypotheses = []
    score = 0

    # 1. Detect payment timeouts.
    payment_timeout = bool(
        re.search(r"payment.{0,50}timeout|timeout.{0,50}payment", text)
    )

    if payment_timeout:
        score += 2
        evidence.append(
            "Payment-related timeout messages appear in the logs."
        )

    # 2. Detect database connection failures.
    db_failure = bool(
        re.search(
            r"database.{0,60}(connection|connect).{0,40}"
            r"(fail|unable|error)|"
            r"unable to acquire database connection",
            text
        )
    )

    if db_failure:
        score += 2
        evidence.append(
            "The logs report database connection acquisition failures."
        )

    # 3. Detect a saturated connection pool.
    pool_saturated = bool(
        re.search(
            r"(connection pool|pool utilization).{0,40}100%",
            text
        )
    )

    if pool_saturated:
        score += 3
        evidence.append(
            "The log reports database connection-pool utilization at 100%."
        )

    # 4. Detect repeated error messages.
    repeated_errors = log_results.get("repeated_errors", {})

    if repeated_errors:
        score += 1
        evidence.append(
            "At least one ERROR message occurs multiple times."
        )

    # 5. Detect explicit high-impact signals.
    critical_patterns = [
        r"\bdata loss\b",
        r"\bsecurity breach\b",
        r"\ball regions down\b",
        r"\bcomplete outage\b",
    ]

    critical_signals = [
        pattern
        for pattern in critical_patterns
        if re.search(pattern, text)
    ]

    if critical_signals:
        evidence.append(
            "The logs contain an explicit high-impact signal: "
            + ", ".join(pattern.replace(r"\b", "") for pattern in critical_signals)
        )

    # 6. Assign a severity with an explanation.
    if critical_signals:
        severity = "Critical"
        rationale = (
            "An explicit high-impact signal was detected. "
            "Verify the signal and assess the real-world impact immediately."
        )
    elif score >= 5:
        severity = "High"
        rationale = (
            f"The rule score is {score}: multiple indicators suggest "
            "a potentially significant service issue."
        )
    elif score >= 2:
        severity = "Medium"
        rationale = (
            f"The rule score is {score}: there are warning signs "
            "that need investigation."
        )
    else:
        severity = "Low"
        rationale = (
            f"The rule score is {score}: few indicators were detected "
            "by the current rules."
        )

    # 7. Generate hypotheses, not confirmed root causes.
    if db_failure and pool_saturated:
        hypotheses.append({
            "cause": "Database connection pool exhaustion",
            "confidence": "Moderate",
            "evidence": [
                "Database connection acquisition failures are present.",
                "Connection-pool utilization is reported at 100%."
            ],
            "next_checks": [
                "Check active, idle, and waiting database connections.",
                "Inspect connection-pool limits and timeout settings.",
                "Look for slow queries or connections that are not released."
            ]
        })

    if payment_timeout:
        hypotheses.append({
            "cause": "Payment requests are waiting too long for a response",
            "confidence": "Low to moderate",
            "evidence": [
                "Payment-related timeout messages are present."
            ],
            "next_checks": [
                "Check payment API latency and timeout metrics.",
                "Review payment-provider status and recent failures.",
                "Compare request IDs with database errors, if available."
            ]
        })

    if not hypotheses:
        hypotheses.append({
            "cause": "Cause not established from the available logs",
            "confidence": "Low",
            "evidence": [
                "The current rules did not find enough evidence "
                "to suggest a specific cause."
            ],
            "next_checks": [
                "Inspect surrounding log entries and timestamps.",
                "Check service health metrics and recent deployments."
            ]
        })

    return {
        "severity": severity,
        "score": score,
        "rationale": rationale,
        "evidence": evidence,
        "hypotheses": hypotheses,
        "critical_signals": critical_signals,
    }
