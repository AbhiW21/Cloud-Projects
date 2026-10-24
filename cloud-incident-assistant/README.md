# Cloud Incident Assistant

An AI-powered cloud troubleshooting prototype that uses **Strands Decider 2B** to select an investigation path and **Amazon Bedrock Nova Lite** to explain the recommendation.

## Problem

When a website experiences HTTP 500 errors alongside high CPU utilization, engineers need to decide where to begin troubleshooting.

## Solution

The application accepts incident log text, analyzes potential issues, recommends an investigation path using Strands Decider, and generates a plain-English explanation using Nova Lite.

## Architecture

```text
Incident Log Text
       |
       v
Streamlit Application
       |
       v
Log Analysis
       |
       v
Strands Decider 2B
       |
       v
Investigation Choice
       |
       v
Amazon Bedrock Nova Lite
       |
       v
Troubleshooting Explanation
```

## Technology Stack

- Python and Streamlit
- Strands Decider 2B
- Amazon Bedrock Nova Lite
- Boto3 and AWS CLI
- Ubuntu and Windows

## Example

**Input:**
```text
ERROR: Website returning HTTP 500
WARNING: CPU utilization is high at 99%
ERROR: Request processing failed
```

**Observed recommendation:** Investigate both application logs and CPU metrics.

Nova Lite explains why checking both can help identify application errors and possible resource pressure.

## Decision Pattern

**Pattern:** Investigation-path classification

Strands Decider selects one of three options:

- `logs` — investigate application logs.
- `metrics` — investigate CPU metrics.
- `both` — investigate both sources.

The decision pattern can be reused in other troubleshooting workflows by changing the question and available choices.

See [`docs/decision-pattern.md`](docs/decision-pattern.md) for implementation details.

## Run Locally

1. Start the Strands Decider server in Ubuntu.
2. Install the Python dependencies listed in `requirements.txt`.
3. Configure valid AWS credentials and Bedrock permissions.
4. Run the Streamlit application:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

5. Open `http://localhost:8501`.
6. 
7. Demo: https://drive.google.com/file/d/1mX8bYyRjKH8kafZjm5c7JpvRG3AyPygX/view?usp=drive_link

## Limitations

- Uses user-provided logs rather than automatically retrieving live CloudWatch data.
- Recommendations are experimental and require further testing.
- Does not automatically fix incidents or remediate AWS resources.

## Future Improvements

- CloudWatch integration.
- Additional incident scenarios and evaluation tests.
- AWS deployment and improved monitoring.

## License

An open-source license will be added before public release.

## Hackathon

Built for the AWS Builder Center Agent Experience Hackathon using Strands Decider 2B.

#strands-decider-2b

## Decision Pattern Documentation

See [Decision Pattern](docs/decision-pattern.md) for the reusable Strands Decider pattern used in this project.
