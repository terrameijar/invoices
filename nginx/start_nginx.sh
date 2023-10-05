#!/bin/bash

ENVIRONMENT="${ENVIRONMENT:-development}"

PRODUCTION_CONFIG="nginx.conf"
DEVELOPMENT_CONFIG="nginx-dev.conf"

if [ "$ENVIRONMENT" = "production" ]; then
    echo "Starting nginx using production config"
    nginx -c /etc/nginx/$PRODUCTION_CONFIG -g "daemon off;"
else

    # Create a self-signed certificate if one doesn't exist
    if [ ! -f /etc/nginx/ssl/invoices_fullchain_dev.pem ]; then
        echo "Creating self-signed certificate"
        mkdir -p /etc/nginx/ssl
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout /etc/nginx/ssl/invoices_privkey.pem \
            -out /etc/nginx/ssl/invoices_fullchain_dev.pem \
            -subj "/CN=localhost"
    fi

    echo "Starting nginx using development config"
    nginx -c /etc/nginx/$DEVELOPMENT_CONFIG -g "daemon off;"
fi
