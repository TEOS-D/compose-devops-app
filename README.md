# Docker Compose Blue-Green DevOps App

Учебный DevOps-проект с Docker Compose, Nginx reverse proxy, HTTPS, blue-green сервисами и Python-приложением.

## Что есть в проекте

- Python app
- Dockerfile с multi-stage build
- запуск контейнера не от root
- Docker Compose
- blue-green сервисы: app-blue и app-green
- Nginx reverse proxy
- HTTPS termination
- HTTP to HTTPS redirect
- Docker DNS
- healthchecks
- restart policy
- resource limits
- named volumes
- env-файлы и `.env.example`

## CI

Проект проверяется через GitHub Actions.

Pipeline выполняет:

- проверку Docker Compose конфигурации
- создание `.env` для CI
- создание временного self-signed сертификата
- сборку Docker images
- запуск сервисов через Docker Compose
- проверку HTTPS health endpoint
- проверку API через Nginx
- проверку HTTP to HTTPS redirect

## Быстрый запуск

```bash
cp .env.example .env
docker compose up -d --build --scale app-blue=2 --scale app-green=2
