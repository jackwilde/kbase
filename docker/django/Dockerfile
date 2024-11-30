FROM python:3.13 AS builder

ENV PATH="/opt/venv/bin:$PATH"

RUN python -m venv /opt/venv

COPY src/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim AS app

LABEL authors="Jack Wilde"
LABEL org.opencontainers.image.source=https://github.com/jackwilde/django-knowledgebase

ARG DJANGO_PROJECT=kbase
ARG DJANGO_USER=django
ENV PATH="/opt/venv/bin:$PATH"

RUN adduser --system \
    --home=/var/opt/$DJANGO_PROJECT \
    --no-create-home \
    --disabled-password \
    --group \
    --shell=/bin/bash $DJANGO_USER

COPY --from=builder /opt/venv /opt/venv
COPY --chown=django:django src /var/opt/${DJANGO_PROJECT}

WORKDIR /var/opt/${DJANGO_PROJECT}

USER ${DJANGO_USER}

COPY --chown=django:django docker/django/start-kbase /usr/local/bin/start-kbase
ENTRYPOINT ["start-kbase"]