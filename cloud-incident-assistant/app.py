"""
Cloud Incident Assistant
------------------------
A beginner-friendly Streamlit app that analyzes AWS cloud incident logs.

Current stage : Demo (no AI or AWS connection yet)
Next steps    : Integrate Amazon Bedrock + Strands Agents SDK
"""

import streamlit as st
import requests
import boto3

# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def detect_issues(log_text: str) -> list[dict]:
    """
    Look for known keywords in the pasted log and return a list of findings.

    Each finding is a small dictionary with three keys:
      - label    : short name shown as a badge (e.g. "Timeout")
      - cause    : plain-English explanation of what probably happened
      - steps    : a list of safe, read-only troubleshooting suggestions

    This is pure Python string-matching — no AI, no AWS calls.
    In a later step we will replace this function with a real AI call.
    """
    findings = []

    # ---- Timeout ----
    if "timed out" in log_text.lower() or "timeout" in log_text.lower():
        findings.append({
            "label": "⏱️ Timeout Detected",
            "cause": (
                "One or more services stopped responding within the allowed time limit. "
                "Common reasons: the function or query is doing too much work, "
                "the downstream service is slow, or memory limits were hit."
            ),
            "steps": [
                "Check the Lambda / ECS task duration in CloudWatch Metrics.",
                "Look for memory pressure — if Memory Used ≈ Memory Size, the function is running out of RAM.",
                "Check if the downstream service (e.g. RDS, DynamoDB) is also showing errors.",
                "Review recent code changes that might have added slower logic.",
            ],
        })

    # ---- High CPU ----
    if "cpu" in log_text.lower() and ("99%" in log_text or "100%" in log_text or "high" in log_text.lower()):
        findings.append({
            "label": "🔥 High CPU Usage",
            "cause": (
                "An EC2 instance is using almost all of its available CPU. "
                "This can cause slowness, timeouts, or crashes for anything running on that machine."
            ),
            "steps": [
                "Go to EC2 → Monitoring tab → check CPU Utilization graph.",
                "Use CloudWatch Logs to find which process is consuming CPU (look for repeated errors).",
                "Check if there was a sudden traffic spike (look at ALB request count).",
                "Consider scaling up the instance type or enabling Auto Scaling (do not change anything yet — confirm with your team first).",
            ],
        })

    # ---- Too many DB connections ----
    if "too many connections" in log_text.lower() or "connection refused" in log_text.lower():
        findings.append({
            "label": "🔌 Database Connection Limit Reached",
            "cause": (
                "The database has hit its maximum number of allowed connections. "
                "New connection attempts are being refused, which will break any feature that reads or writes data."
            ),
            "steps": [
                "Check RDS → Monitoring → DatabaseConnections metric in CloudWatch.",
                "Identify which application or Lambda is opening the most connections.",
                "Look for connection leaks — connections that are opened but never closed.",
                "Consider using RDS Proxy to pool connections (discuss with your team before changing).",
            ],
        })

    # ---- Unhealthy targets / ALB ----
    if "unhealthy" in log_text.lower() or "healthyHostCount: 0" in log_text or "HealthyHostCount: 0" in log_text:
        findings.append({
            "label": "🚨 All Targets Unhealthy (ALB)",
            "cause": (
                "The Application Load Balancer cannot find any healthy servers to send traffic to. "
                "Users will see errors (502/503) until at least one target becomes healthy again."
            ),
            "steps": [
                "Open EC2 → Target Groups → check the health status of each target.",
                "Review the health check path — make sure the app is returning HTTP 200 on that path.",
                "Check EC2 instance logs for crash messages or out-of-memory errors.",
                "Verify security group rules allow the ALB to reach the instances on the health-check port.",
            ],
        })

    # ---- Generic status check failure ----
    if "statuscheckfailed" in log_text.lower() or "reachability check failed" in log_text.lower():
        findings.append({
            "label": "❌ EC2 Instance Unreachable",
            "cause": (
                "AWS cannot reach the EC2 instance. This could mean the OS crashed, "
                "the network interface lost connectivity, or the underlying hardware has an issue."
            ),
            "steps": [
                "Go to EC2 Console → select the instance → Actions → Monitor and troubleshoot → Get system log.",
                "Check EC2 → Status Checks tab for which check is failing (System vs Instance).",
                "If it is a System check failure, try stopping and starting the instance (NOT reboot) to move it to new hardware.",
                "If it is an Instance check failure, review the OS-level logs for kernel panics or disk-full errors.",
            ],
        })

    return findings
    
def ask_decider(log_text: str) -> dict:
    """Ask Strands Decider which investigation path to follow."""
    payload = {
        "state": log_text,
        "questions": {
            "investigation": {
                "type": "choice",
                "instructions": "What should we investigate first?",
                "criteria": {
                    "logs": "Investigate application logs.",
                    "metrics": "Investigate CPU utilization metrics.",
                    "both": "Investigate both application logs and CPU metrics."
                }
            }
        }
    }

    response = requests.post(
        "http://localhost:8000/v1/systemone",
        json=payload,
        timeout=90
    )
    response.raise_for_status()
    return response.json()

def explain_recommendation(log_text, choice):
    """Use Amazon Bedrock Nova Lite to explain the recommendation."""
    client = boto3.client(
        "bedrock-runtime",
        region_name="ap-south-1"
    )

    labels = {
        "logs": "application logs",
        "metrics": "CPU metrics",
        "both": "both application logs and CPU metrics"
    }

    selected = labels.get(choice, choice)

    response = client.converse(
        modelId="apac.amazon.nova-lite-v1:0",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": (
                            "You are a cloud incident troubleshooting assistant. "
                            "Explain in simple English why this investigation "
                            "choice is useful. Do not claim you have inspected "
                            "real AWS resources. Keep the answer under 100 words.\n\n"
                            f"Incident logs:\n{log_text[:3000]}\n\n"
                            f"Recommended investigation: {selected}"
                        )
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 120,
            "temperature": 0.2
        }
    )

    return response["output"]["message"]["content"][0]["text"]



# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Cloud Incident Assistant",
    page_icon="☁️",
    layout="centered",
)

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------

st.title("☁️ Cloud Incident Assistant")
st.caption("AWS Hackathon Project — Demo Stage (no AI or AWS connection yet)")

st.markdown(
    """
    Paste your AWS log output below and click **Analyze**.
    The assistant will highlight possible causes and safe troubleshooting steps.

    > 💡 **Tip:** Open `sample_logs.txt` in this folder and paste its contents to try a demo.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# LOG INPUT
# ---------------------------------------------------------------------------

log_input = st.text_area(
    label="Paste your log here",
    placeholder="e.g.  2024-10-19T10:03:15Z ERROR [Lambda] Task timed out after 30.00 seconds",
    height=220,
    help="Paste any CloudWatch log, EC2 system log, or Lambda log excerpt.",
)

analyze_button = st.button("🔍 Analyze Log", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# ANALYSIS OUTPUT
# ---------------------------------------------------------------------------

if analyze_button:
    if not log_input.strip():
        # If the user clicked Analyze without pasting anything, show a warning.
        st.warning("Please paste a log before clicking Analyze.")
    else:
        st.divider()
        st.subheader("📋 Analysis Results")
        
        # Ask Strands Decider for an investigation recommendation
        try:
            with st.spinner("Strands Decider is choosing an investigation path..."):
                result = ask_decider(log_input)

            answer = result.get("answers", {}).get("investigation", {})
            choice = answer.get("choice", "unknown")
            confidence = answer.get("confidence")
            probabilities = answer.get("probabilities", {})

            labels = {
                "logs": "Application logs",
                "metrics": "CPU metrics",
                "both": "Both logs and metrics",
            }

            st.subheader("🧭 Strands Decider Recommendation")
            st.write(f"**Investigation path:** {labels.get(choice, choice)}")

            if confidence is not None:
                st.write(f"Model confidence: {confidence:.1%}")

            if probabilities:
                st.caption("Choice probabilities (experimental)")
                st.json(probabilities)

            # Ask Nova Lite to explain the recommendation
            try:
                with st.spinner("Nova Lite is explaining the recommendation..."):
                    explanation = explain_recommendation(log_input, choice)

                st.subheader("💡 AI Troubleshooting Explanation")
                st.write(explanation)

            except Exception as exc:
                st.warning(f"Nova Lite explanation unavailable: {exc}")


        except requests.RequestException as exc:
            st.warning(
                "Strands Decider could not be reached. "
                "Check that the Ubuntu server is still running. "
                f"Details: {exc}"
            )


        # Small disclaimer so it is clear this is a demo
        st.info(
            "🚧 **Demo mode** — Results are based on keyword matching, not AI. "
            "Amazon Bedrock + Strands Agents integration coming in the next step.",
            icon="ℹ️",
        )

        findings = detect_issues(log_input)

        if not findings:
            # No known keywords matched
            st.success(
                "No common issues detected in the pasted log. "
                "The log may be healthy, or it may contain an issue this demo version does not recognise yet. "
                "The AI-powered version will handle a much wider range of scenarios."
            )
        else:
            st.markdown(f"**{len(findings)} issue(s) found:**")

            for finding in findings:
                # Each issue gets its own expandable card
                with st.expander(finding["label"], expanded=True):

                    st.markdown("**Possible Cause**")
                    st.write(finding["cause"])

                    st.markdown("**Safe Troubleshooting Steps**")
                    for step in finding["steps"]:
                        st.markdown(f"- {step}")

        st.divider()
        st.caption(
            "Next milestone: connect to Amazon Bedrock (Claude via Strands Agents SDK) "
            "for deep, context-aware analysis and automated runbook suggestions."
        )
