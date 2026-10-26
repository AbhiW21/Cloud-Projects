# Linux Server Health Monitoring

## Overview
A Bash-based Linux administration project that collects system health information and checks disk and memory usage against configurable warning thresholds.

## Features
- System uptime reporting
- Memory usage reporting
- Disk space reporting
- Top CPU-consuming process reporting
- Configurable disk and memory warning thresholds
- Timestamped health reports
- Final health status summary

## Technologies
- Red Hat Enterprise Linux 9
- Bash scripting
- Linux command-line utilities
- Git and GitHub

## How to Run
From the project directory on Linux:

```bash
bash scripts/health_check.sh
```

Reports are saved in the `logs/` directory.

## Warning Thresholds
The default disk and memory warning thresholds are 80%.

## Limitations
This project generates local reports when manually run. It does not continuously monitor the server or send notifications.
