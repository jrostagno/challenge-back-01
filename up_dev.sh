#!/usr/bin/env bash
set -e

echo "running docker compose"

docker compose -f docker-compose.yml up --build
