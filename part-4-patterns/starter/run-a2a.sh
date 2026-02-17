#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Cleanup background processes on exit
cleanup() {
    echo "Shutting down agents..."
    [[ -n "${CRITIC_PID:-}" ]] && kill "$CRITIC_PID" 2>/dev/null
    [[ -n "${PLANNER_PID:-}" ]] && kill "$PLANNER_PID" 2>/dev/null
    wait "$CRITIC_PID" 2>/dev/null
    wait "$PLANNER_PID" 2>/dev/null
    echo "Done."
}
trap cleanup EXIT

wait_for_port() {
    local port=$1
    local retries=30
    while ! curl -sf "http://127.0.0.1:${port}/.well-known/agent-card.json" >/dev/null 2>&1; do
        retries=$((retries - 1))
        if [[ $retries -le 0 ]]; then
            echo "ERROR: agent on port ${port} failed to start"
            exit 1
        fi
        sleep 1
    done
}

echo "Starting Critic agent on port 9001..."
python "$SCRIPT_DIR/a2a/agent-critic.py" &
CRITIC_PID=$!
wait_for_port 9001
echo "Critic agent is ready."

echo "Starting Planner agent on port 9002..."
python "$SCRIPT_DIR/a2a/agent-planner.py" &
PLANNER_PID=$!
wait_for_port 9002
echo "Planner agent is ready."

# 3. Run the A2A client
echo "Running agent-to-agent-a2a client..."
python "$SCRIPT_DIR/agent-to-agent-a2a.py"
