#!/bin/bash

# Dynamically load config into Nginx byt symlinking from conf-available to conf-enabled


# Change include path in nginx.conf
sed -i 's/conf.d/conf-enabled/' /etc/nginx/nginx.conf

# Check that the certificate and key exist
if [[ -e /etc/nginx/ssl/server.pem && -e /etc/nginx/ssl/server.key ]]; then
  echo "Certificate and key provided. Enabling SSL."
  ln -s /etc/nginx/conf-available/ssl.conf /etc/nginx/conf-enabled/
else
  echo "No Certificate and key provided. Starting with HTTP."
  ln -s /etc/nginx/conf-available/default.conf /etc/nginx/conf-enabled/
fi

# Add security conf
ln -s /etc/nginx/conf-available/security.conf /etc/nginx/conf-enabled/

exit 0

