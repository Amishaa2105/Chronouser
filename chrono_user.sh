#!/bin/bash

# Path to store user activity logs
LOG_FILE="./logs/user_activity.log"

log_user_activity() {
    local USERNAME=$(whoami)
    local TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    local ACTION=$1
    echo "$TIMESTAMP, $USERNAME, $ACTION" >> "$LOG_FILE"
}

log_user_activity "LOGIN"

trap 'log_user_activity "LOGOUT"; exit' EXIT

while true; do
    sleep 60  # Wait for 60 seconds before checking idle state

    IDLE_TIME=$(xprintidle 2>/dev/null || echo 0)

    if [ "$IDLE_TIME" -gt 60000 ]; then
        log_user_activity "IDLE"
    else
        log_user_activity "ACTIVE"
    fi
done