#!/bin/bash

ENVIRONMENT="${ENVIRONMENT:-development}"

PRODUCTION_CONFIG="nginx.conf"
DEVELOPMENT_CONFIG="nginx-dev.conf"

if [ "$ENVIRONMENT" = "production" ]; then
    echo "Starting nginx using production config"
    nginx -c /etc/nginx/$PRODUCTION_CONFIG -g "daemon off;"
else
    echo "Starting nginx using development config"
    nginx -c /etc/nginx/$DEVELOPMENT_CONFIG -g "daemon off;"
fi
