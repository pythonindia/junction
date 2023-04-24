#!/bin/bash
# wait-for-it.sh: Wait for a service to be ready.

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$host" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
