#!/bin/sh

echo "Waiting for mongo..."
echo "Waiting for RabbitMQ..."

while ! nc -z $MONGO_HOST $MONGO_PORT; do
  sleep 0.1
done
echo "MongoDB started"

while ! nc -z $RABBIT_HOST 15672; do
  sleep 0.1
done
echo "RabbitMQ started"

python main.py || return

exec "$@"