#!/bin/bash
set -e

echo "[*] Running in STANDALONE mode"
python3 -u /app/fuzz.py /app/config_docker.txt -o /app/fume_sync