#!/bin/bash

# Linux Server Health Monitoring
# Project: AbhiW

DISK_THRESHOLD=80
MEMORY_THRESHOLD=80

REPORT="logs/health_report_$(date +%Y%m%d_%H%M%S).txt"

mkdir -p logs
WARNINGS=0

{
    echo "===== LINUX SERVER HEALTH REPORT ====="
    echo "Date: $(date)"
    echo "Hostname: $(hostname)"
    echo

    echo "===== SYSTEM UPTIME ====="
    uptime
    echo

    echo "===== MEMORY USAGE ====="
    free -h
    echo

    echo "===== DISK USAGE ====="
    df -h
    echo

    echo "===== TOP PROCESSES ====="
    ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 6
    echo

    echo "===== DISK HEALTH CHECK ====="

    while read -r usage mountpoint; do
        usage=${usage%\%}

        if (( usage >= DISK_THRESHOLD )); then
            echo "WARNING: Disk usage is ${usage}% on ${mountpoint}"
            WARNINGS=$((WARNINGS + 1))
        fi
    done < <(df -P -x tmpfs -x devtmpfs |
             awk 'NR > 1 {print $5, $6}')

    echo
    echo "===== MEMORY HEALTH CHECK ====="

    MEMORY_USAGE=$(free -b | awk '/^Mem:/ {
        if ($2 > 0)
            printf "%d", (($2 - $7) / $2) * 100
    }')

    echo "Memory usage: ${MEMORY_USAGE}%"

    if (( MEMORY_USAGE >= MEMORY_THRESHOLD )); then
        echo "WARNING: Memory usage is high!"
        WARNINGS=$((WARNINGS + 1))
    fi

    echo
    echo "===== FINAL STATUS ====="

    if (( WARNINGS > 0 )); then
        echo "WARNING: ${WARNINGS} health warning(s) detected."
    else
        echo "OK: No disk or memory warnings detected."
    fi

} > "$REPORT"

echo "Health report generated: $REPORT"

if (( WARNINGS > 0 )); then
    echo "WARNING: ${WARNINGS} health warning(s) detected."
else
    echo "OK: No disk or memory warnings detected."
fi
