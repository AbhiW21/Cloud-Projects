\# Reusable Decision Pattern: Incident Investigation Path



\## Purpose



This pattern uses Strands Decider 2B to select an initial investigation path for a cloud incident.



\## Decision Type



\*\*Type:\*\* Multiple-choice decision



\*\*State:\*\* User-provided incident log text.



\*\*Question:\*\* What should we investigate first?



\## Available Choices



| Choice | Description |

|---|---|

| `logs` | Investigate application logs. |

| `metrics` | Investigate CPU utilization metrics. |

| `both` | Investigate both application logs and CPU metrics. |



\## Typed Question



```json

{

&#x20; "state": "Website returns HTTP 500 errors and CPU usage is high.",

&#x20; "questions": {

&#x20;   "investigation": {

&#x20;     "type": "choice",

&#x20;     "instructions": "What should we investigate first?",

&#x20;     "criteria": {

&#x20;       "logs": "Investigate application logs for HTTP 500 errors.",

&#x20;       "metrics": "Investigate CPU utilization metrics.",

&#x20;       "both": "Investigate both application logs and CPU metrics."

&#x20;     }

&#x20;   }

&#x20; }

}

```



\## How the Pattern Works



1\. Receive incident log text from the application.

2\. Send the incident state and typed question to the Strands Decider API.

3\. Read the selected choice and its confidence information.

4\. Pass the recommendation to Amazon Bedrock Nova Lite for a plain-English explanation.

5\. Display the recommendation and explanation to the user.



\## Example



For an incident containing HTTP 500 errors and high CPU utilization, the initial test selected `both`.



This is an observed test result, not a guaranteed outcome for every incident.



\## Reuse in Another Agent



To reuse this pattern:



1\. Provide the incident state as text.

2\. Define a typed `choice` question and meaningful options.

3\. Send the request to a configured Strands Decider endpoint.

4\. Handle the returned choice, probabilities, and confidence.

5\. Connect the result to your own investigation workflow.



Change the question and options to fit your use case. Test multiple scenarios before relying on the result.



\## Wiring in This Project



The Streamlit application calls the local Strands Decider API at `/v1/systemone` using `requests`. The returned choice is then passed to the `explain\_recommendation()` function, which calls Amazon Bedrock Nova Lite.



\## Limitations



This pattern recommends an investigation path; it does not fetch live CloudWatch data, establish root cause, or remediate an incident automatically.



Strands Decider 2B is experimental. Evaluate its accuracy and low-confidence behavior before using the pattern in other applications.



