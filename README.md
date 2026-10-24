# AI Incident Log Analyzer

A Python and Streamlit application that analyzes application logs, identifies recurring errors, estimates incident severity, and generates evidence-based troubleshooting suggestions using an optional LLM API.

## Features

- Upload `.log` and `.txt` files or paste log content.
- Count ERROR, WARN, INFO, and DEBUG messages.
- Identify repeated error messages.
- Estimate incident severity using transparent rules.
- Separate observed log evidence from possible root causes.
- Generate AI-assisted incident summaries and investigation steps.
- Fall back to rule-based analysis when AI analysis is unavailable.
- Treat log contents as untrusted input.

## Technology Stack

- Python
- Streamlit
- Regular expressions
- OpenAI Python SDK and Responses API
- python-dotenv
- pytest

## Architecture

1. **Streamlit UI:** Accepts log files or pasted log text.
2. **Log Processor:** Extracts severity levels, counts messages, and identifies repeated errors.
3. **Incident Analyzer:** Applies deterministic rules to estimate severity and produce root-cause hypotheses.
4. **AI Analyzer:** Sends a limited log excerpt and existing findings to the configured LLM for further analysis.
5. **Fallback:** Preserves the rule-based assessment when AI analysis fails.
6. **Tests:** Validate parsing, severity rules, and missing-API-key behavior.

## Prerequisites

- Python 3.11 or later
- pip
- An API key for AI analysis, if that feature is required

## Setup

Clone the repository and enter its directory:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-incident-log-analyzer
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root if you want AI analysis:

```dotenv
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=your_supported_model
```

Use a model available to your API account. Never commit `.env` or publish your API key.

## Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed by Streamlit.

## Run Tests

```bash
python -m pytest -v
```

## Sample Scenarios

The `sample_logs/` directory contains simulated examples for database connection failures, application recovery, and untrusted log content.

## Severity Rules

Severity is estimated using predefined indicators such as payment timeouts, database connection failures, connection-pool saturation, repeated errors, and explicit high-impact phrases.

These rules are educational examples, not universal incident-severity standards. Real severity should also account for service criticality, duration, scope, and confirmed business impact.

## Security and Limitations

- Treat log content as untrusted data.
- Do not submit real production logs containing secrets or personal data without authorization and appropriate safeguards.
- The AI receives a limited excerpt of the supplied logs; the API may incur charges.
- Prompt instructions reduce risk but do not eliminate prompt injection.
- AI-generated root causes are hypotheses, not confirmed diagnoses.
- Severity estimates require human verification.
- The application does not independently query live infrastructure or execute remediation.

## Future Improvements

- Support additional log formats and structured JSON logs.
- Add timestamps, correlation IDs, and service-level filtering.
- Improve severity rules using service impact and incident duration.
- Add redaction of sensitive information before external API calls.
- Add structured AI output validation and stronger security tests.
- Add monitoring dashboards and deployment automation.

## Disclaimer

This project is a learning and demonstration tool. Validate findings before taking operational action.
