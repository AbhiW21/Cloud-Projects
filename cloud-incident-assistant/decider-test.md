# Strands Decider 2B — Initial Test

## Project
Cloud Incident Assistant

## Objective
Test whether Strands Decider can select an investigation approach for a cloud incident.

## Test Scenario
The website returns HTTP 500 errors, and CPU usage is high.

## Available Choices
- Application logs
- CPU metrics
- Both logs and metrics

## Observed Result
The Decider selected **both logs and metrics**.

## Why This Matters
Logs help investigate application errors, while CPU metrics help identify resource pressure. Checking both provides a broader view of the incident.

## Status
Initial command-line test completed successfully.

## Next Step
Integrate the Decider with the Cloud Incident Assistant and connect Amazon Bedrock for troubleshooting explanations.
