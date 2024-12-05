# Docker

## Introduction
The kbase application is designed to run as a container. In production scenarios Kubernetes is the recommended method 
of deployment. Docker provides a great ran to run this application on a small scare and test or dev environment. The
steps required to run kbase with Docker are listed here.

## Deployment
1. Clone this repository to a local directory \
   `git clone https://github.com/jackwilde/kbase.git`
2. Go to the [docker](./) directory \
    `cd kbase/docker`
3. Create a file called .env for required secure environment variables and add the following and set the variables with 
   values.
   ```
   SECRET_KEY=<secret_key>
   POSTGRES_DB=<postgres_database_name>
   POSTGRES_USER=<postgres_user>
   POSTGRES_PASSWORD=<postgres_user_password>
   ```
4. _(Optional)_ Edit [docker-compose.yaml](./docker-compose.yaml) to suit requirements
5. Start the application \
   `docker compose up -d --build`

This will start the application and by default it will be available on http://localhost:8080

## Customisation
To customise the deployment edit the [docker-compose.yaml](./docker-compose.yaml) to suit requirements. \
A few specific customisations are listed below.
### Enable SSL
By default, the application will run using unencrypted http. While this is fine for test deployments if you want to
secure it with SSL simply add the certificate and key to the nginx service volumes, as in this example:
```
  nginx:
    volumes:
      - "static:/usr/share/nginx/html/static/"
      - "./nginx/conf-available/:/etc/nginx/conf-available/"
      - "./nginx/docker-entrypoint.d:/docker-entrypoint.d/"
      - "nginx-conf:/etc/nginx/conf-enabled/"
      - "/path/to/certificate.pem:/etc/nginx/ssl/server.pem"
      - "/path/to/private.key:/etc/nginx/ssl/server.key"
```
On startup if Nginx detects a certificate and key at those paths it will enable SSL and the application will be
available https://host.domain.com:8443 

### Default Ports
By default, the application will run on 8080 for http connections and 8443. You can customise this in the ports section
of the Nginx service, as in this example:
```
nginx:
      ports:
      - "443:443"
      - "80:80"
```
Changing the first value for each port will change the port the host is listening on. This example would set the host to
respond to the default 80 and 443 ports for http and https connections.