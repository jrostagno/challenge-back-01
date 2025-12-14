#!/usr/bin/env bash
set -e

echo "running tests..."

docker compose -p challenge_test \
  --env-file .env.test \
  -f docker-compose.test.yml \
  up --build --abort-on-container-exit

echo "🧹 cleaning containers and volumes..."

docker compose -p challenge_test \
  -f docker-compose.test.yml \
  down -v
