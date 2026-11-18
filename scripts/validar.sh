#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose -f compose.yaml -f compose.lab.yaml config --quiet
echo '[1/5] Compose valido'
docker compose -f compose.yaml -f compose.lab.yaml ps
echo '[2/5] Liveness e readiness'
curl -fsS http://127.0.0.1:${APP_PORT:-8081}/api/live; echo
curl -fsS http://127.0.0.1:${APP_PORT:-8081}/api/ready; echo
echo '[3/5] Informacoes de deploy'
curl -fsS http://127.0.0.1:${APP_PORT:-8081}/api/info; echo
echo '[4/5] Lista de tarefas'
curl -fsS http://127.0.0.1:${APP_PORT:-8081}/api/tasks; echo
echo '[5/5] Concluido - registrar evidencias'
