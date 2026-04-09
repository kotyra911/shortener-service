#!/bin/bash
set -e

DB_TEST="${POSTGRES_DB}_test"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

CREATE TABLE IF NOT EXISTS links (
  link_id SERIAL PRIMARY KEY,
  original_link TEXT NOT NULL,
  short_key VARCHAR(6) NOT NULL UNIQUE,
  clicks BIGINT DEFAULT 0
);

EOSQL


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

SELECT 'CREATE DATABASE ${DB_TEST}'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = '${DB_TEST}'
)\gexec

EOSQL


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_TEST" <<-EOSQL

CREATE TABLE IF NOT EXISTS links (
  link_id SERIAL PRIMARY KEY,
  original_link TEXT NOT NULL,
  short_key VARCHAR(6) NOT NULL UNIQUE,
  clicks BIGINT DEFAULT 0
);

EOSQL
