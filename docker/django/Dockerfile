FROM python:3.13-slim

LABEL authors="Jack Wilde"
LABEL org.opencontainers.image.source=https://github.com/jackwilde/django-knowledgebase

ARG DJANGO_PROJECT=kbase
ARG DJANGO_USER=django

RUN apt update && \
    apt-get install -y --no-install-recommends\
      postgresql-client \
      libpq-dev && \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --system \
    --home=/var/opt/$DJANGO_PROJECT \
    --no-create-home \
    --disabled-password \
    --group \
    --shell=/bin/bash $DJANGO_USER

COPY --chown=django:django src /var/opt/${DJANGO_PROJECT}

WORKDIR /var/opt/${DJANGO_PROJECT}

RUN pip install --no-cache-dir -r requirements.txt

USER ${DJANGO_USER}

COPY --chown=django:django docker/django/start-kbase /usr/local/bin/start-kbase
ENTRYPOINT ["start-kbase"]