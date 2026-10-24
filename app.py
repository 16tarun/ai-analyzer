
import streamlit as st

from log_processor import analyze_logs
from incident_analyzer import analyze_incident
from ai_analyzer import analyze_with_ai


st.set_page_config(
    page_title="AI Incident Log Analyzer",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ AI Incident Log Analyzer")

st.write(
    "Analyze application logs, identify likely causes, "
    "and recommend troubleshooting steps."
)

st.info("Use sample or simulated logs only.")

uploaded_file = st.file_uploader(
    "Upload an application log file (maximum 5 MB)",
    type=["log", "txt"],
    max_upload_size=5
)

logs = st.text_area(
    "Or paste your application logs here",
    height=250,
    placeholder="Paste your logs here..."
)

if uploaded_file is not None:
    logs = uploaded_file.getvalue().decode(
        "utf-8",
        errors="replace"
    )


if st.button("Analyze Logs", type="primary"):

    if logs.strip():

        # Stage 3: Process logs
        results = analyze_logs(logs)

        # Stage 4: Assess severity and hypotheses
        incident = analyze_incident(logs, results)

        # Stage 5: Generate AI analysis
        with st.spinner("Analyzing incident..."):
            ai_result = analyze_with_ai(
                logs,
                results,
                incident
            )

        # -----------------------------------------
        # 1. LOG SUMMARY
        # -----------------------------------------
        st.subheader("Log Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Lines",
            results["total_lines"]
        )

        col2.metric(
            "Errors",
            results["error_count"]
        )

        col3.metric(
            "Warnings",
            results["warning_count"]
        )

        col4.metric(
            "Info Messages",
            results["info_count"]
        )

        # -----------------------------------------
        # 2. INCIDENT SEVERITY
        # -----------------------------------------
        st.subheader("Incident Assessment")

        severity = incident["severity"]

        if severity == "Critical":
            st.error(f"🔴 Severity: {severity}")

        elif severity == "High":
            st.warning(f"🟠 Severity: {severity}")

        elif severity == "Medium":
            st.info(f"🟡 Severity: {severity}")

        else:
            st.success(f"🟢 Severity: {severity}")

        st.metric(
            "Incident Rule Score",
            incident["score"]
        )

        st.write("**Severity rationale**")
        st.write(incident["rationale"])

        # -----------------------------------------
        # 3. EVIDENCE FROM LOGS
        # -----------------------------------------
        st.subheader("Evidence from Logs")

        if incident["evidence"]:
            for item in incident["evidence"]:
                st.markdown(f"- {item}")

        else:
            st.write(
                "No specific evidence matched the current rules."
            )

        # -----------------------------------------
        # 4. POSSIBLE ROOT CAUSES
        # -----------------------------------------
        st.subheader("Possible Root Causes")

        st.caption(
            "These are hypotheses, not confirmed root causes. "
            "Verify them using metrics and additional logs."
        )

        for index, hypothesis in enumerate(
            incident["hypotheses"],
            start=1
        ):

            with st.expander(
                f"{index}. {hypothesis['cause']} "
                f"({hypothesis['confidence']} confidence)",
                expanded=True
            ):

                st.write("**Supporting evidence**")

                for item in hypothesis["evidence"]:
                    st.markdown(f"- {item}")

                st.write("**Recommended investigation steps**")

                for item in hypothesis["next_checks"]:
                    st.markdown(f"- {item}")

        # -----------------------------------------
        # 5. AI-POWERED ANALYSIS
        # -----------------------------------------
        st.subheader("AI-Powered Incident Analysis")

        if ai_result["ok"]:

            st.success("AI analysis completed successfully.")

            st.markdown(ai_result["analysis"])

        else:

            st.warning(
                "AI analysis is unavailable. "
                "Showing the rule-based assessment instead."
            )

            st.caption(ai_result["error"])

            st.write("**Current severity:**", incident["severity"])

            st.write("**Reason:**", incident["rationale"])

            st.write("**Evidence detected by rules:**")

            if incident["evidence"]:
                for item in incident["evidence"]:
                    st.markdown(f"- {item}")

            else:
                st.write(
                    "No specific evidence matched the current rules."
                )

        # -----------------------------------------
        # 6. DETECTED ERRORS
        # -----------------------------------------
        st.subheader("Detected Errors")

        if results["error_messages"]:

            for error in results["error_messages"]:
                st.error(error)

        else:
            st.success("No ERROR-level messages detected.")

        # -----------------------------------------
        # 7. REPEATED ERRORS
        # -----------------------------------------
        st.subheader("Repeated Errors")

        if results["repeated_errors"]:

            for message, count in (
                results["repeated_errors"].items()
            ):

                st.write(f"**Occurrences: {count}**")
                st.code(message, language="text")

        else:
            st.write("No repeated errors detected.")

        # -----------------------------------------
        # 8. INPUT PREVIEW
        # -----------------------------------------
        st.subheader("Input Preview")

        st.code(logs[:5000], language="text")

        st.caption(
            "Severity and root-cause hypotheses are estimates. "
            "Verify findings against actual service impact."
        )

    else:
        st.warning(
            "Please upload a file or paste some logs."
        )
