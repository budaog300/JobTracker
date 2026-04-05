#!/bin/bash
set -e

echo "Migrations apply..."
alembic upgrade head

echo "Starting application..."
exec "$@"