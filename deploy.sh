#!/bin/bash
# Replace with the actual path where your board mounts
TARGET="/Volumes/CIRCUITPY"

if [ -d "$TARGET" ]; then
    echo "Deploying code to CircuitPython board..."
    cp -r src/* "$TARGET/"
    echo "Deployment complete!"
else
    echo "Error: CIRCUITPY drive not found. Is it plugged in?"
fi
