FROM nginx:1.27
LABEL authors="Jack Wilde"

COPY --chown=nginx:nginx src/static/ /usr/share/nginx/html/static/
COPY --chown=nginx:nginx docker/nginx/conf.d/ /etc/nginx/conf.d/
COPY --chown=root:root docker/nginx/docker-entrypoint.d/50-configure-ssl.sh /docker-entrypoint.d/

RUN mkdir /etc/nginx/ssl