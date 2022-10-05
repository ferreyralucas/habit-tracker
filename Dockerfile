FROM python:3.10.7-slim-buster

# Define ARGs
ARG ENVIRONMENT=default

# Python logs to STDOUT
ENV PYTHONUNBUFFERED 1

# Sane defaults for pip
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements/*.txt /tmp/requirements/

RUN set -x \
    && buildDeps=" \
    libffi-dev \
    libpq-dev \
    python3-dev \
    binutils \
    musl-dev \
    openssh-client \
    git \
    " \
    && runDeps=" \
    postgresql-client \
    gcc \
    unrar \
    " \
    && echo "deb http://deb.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps \
    && apt-get install -y --no-install-recommends $runDeps \
    # Install Python dependencies
    && pip install -r /tmp/requirements/base.txt \
    && if [ $ENVIRONMENT = local ]; then \
    # Install python dev dependencies
    pip install -r /tmp/requirements/test.txt \
    && pip install -r /tmp/requirements/dev.txt; \
    # Install dependencies for graphviz
    # apt-get install graphviz graphviz-dev ttf-freefont; \
    else \
    # other environment to local remove the build dependencies
    apt-get remove -y $buildDeps; \
    fi \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Work dir and copy code.
WORKDIR /app
COPY . .

# add our user and group first to make sure their IDs get assigned consistently
RUN groupadd -r deployer && useradd -r -m -g deployer deployer && chown -R deployer:deployer /app

# USER deployer

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
