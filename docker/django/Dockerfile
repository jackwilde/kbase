FROM python:3.13

LABEL authors="Jack Wilde"
LABEL org.opencontainers.image.source=https://github.com/jackwilde/django-knowledgebase

ARG DJANGO_PROJECT=kbase
ARG DJANGO_USER=django

# Install postgres client, used for checking DB status
RUN apt update && \
    apt-get install -y --no-install-recommends \
      postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Create non root user to run the app
RUN adduser --system \
    --home=/var/opt/$DJANGO_PROJECT \
    --no-create-home \
    --disabled-password \
    --group \
    --shell=/bin/bash $DJANGO_USER

# Copy app code
COPY --chown=django:django src /var/opt/${DJANGO_PROJECT}

# Set workdir to application directory
WORKDIR /var/opt/${DJANGO_PROJECT}

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run application tests
RUN python manage.py test --noinput

# Set container user to $DJANO_USER
USER ${DJANGO_USER}

# Copy and and set entrypoint script
COPY --chown=django:django docker/django/start-kbase /usr/local/bin/start-kbase
ENTRYPOINT ["start-kbase"]