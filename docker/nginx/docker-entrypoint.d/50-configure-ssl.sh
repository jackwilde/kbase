#!/bin/bash

# Check if SSL is enabled
if [[ $ENABLE_SSL == "True" ]]; then
  error=0
  echo "ENABLE_SSL is True..."
  echo "Checking for certificates..."

  # Check that the certificate and key exist
  if [[ ! -e /etc/nginx/ssl/server.pem ]]; then
    echo "SSL certificate is missing..."
    echo "Add the certificate to /etc/nginx/ssl/server.pem"
    error=1
  fi

  if [[ ! -e /etc/nginx/ssl/server.key ]]; then
    echo "SSL key is missing..."
    echo "Add the key to /etc/nginx/ssl/server.key"
    error=1
  fi

  # If either check errored then exit
  if [[ $error -ne 0 ]]; then
    exit 1
  fi

  echo "Disabling non-SSL config"
  # Remove the non ssl config
  rm /etc/nginx/conf.d/default.conf

else
  echo "ENABLE_SSL is not True.."
  echo "Disabling SSL config"
  # Remove the SSL config if SSL is not enabled
  rm /etc/nginx/conf.d/ssl.conf
fi

exit 0