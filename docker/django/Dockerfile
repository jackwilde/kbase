FROM python:3.13
LABEL authors="Jack Wilde"

ARG DJANGO_PROJECT=django-knowledgebase
ARG DJANGO_USER=django

RUN adduser --system \
    --home=/var/opt/$DJANGO_PROJECT \
    --no-create-home \
    --disabled-password \
    --group \
    --shell=/bin/bash $DJANGO_USER


COPY --chown=django:django src /var/opt/${DJANGO_PROJECT}

WORKDIR /var/opt/${DJANGO_PROJECT}

RUN pip install -r requirements.txt

USER ${DJANGO_USER}

COPY --chown=django:django docker/django/start-kbase /usr/local/bin/start-kbase
ENTRYPOINT ["start-kbase"]