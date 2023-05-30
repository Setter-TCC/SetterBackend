#!/bin/bash

# Exporting all environment variables to use in crontab
env | sed 's/^\(.*\)$/ \1/g' > /root/env

# Função que espera o postgres ficar pronto antes de subir o server
function_postgres_ready() {
python << END
import socket
import time
import os

port = int(5432)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('10.5.0.6', port))
s.close()
END
}

echo '======= CHECKING FOR UNINSTALLED PKGs AND INSTALLING'
pip install -r requirements.txt

until function_postgres_ready; do
  >&2 echo "======= POSTGRES IS UNAVAILABLE, WAITING"
  sleep 1
done
echo "======= POSTGRES IS UP, CONNECTING"

echo '======= MAKING MIGRATIONS'
alembic upgrade head

echo '======= RUNNING SERVER'
uvicorn src.main:app --host 0.0.0.0 --port 8000