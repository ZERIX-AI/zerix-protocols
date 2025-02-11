# base image
FROM python:3.10-slim-bookworm AS base

WORKDIR /app/api

# Install Poetry
ENV POETRY_VERSION=1.8.3

# Use official mirror for pip install
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# Configure Poetry
ENV POETRY_CACHE_DIR=/tmp/poetry_cache
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_REQUESTS_TIMEOUT=15

FROM base AS packages

# Use official debian mirror
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ libc-dev libffi-dev libgmp-dev libmpfr-dev libmpc-dev

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-cache --no-root

# production stage
FROM base AS production

ENV FLASK_APP=app.py
ENV EDITION=SELF_HOSTED
ENV DEPLOY_ENV=PRODUCTION
ENV CONSOLE_API_URL=https://test-ai.zerix.io/backend
ENV CONSOLE_WEB_URL=https://test-ai.zerix.io
ENV SERVICE_API_URL=https://test-ai.zerix.io/backend
ENV APP_WEB_URL=https://test-ai.zerix.io

EXPOSE 5001

# set timezone
ENV TZ=UTC

WORKDIR /app/api

RUN apt-get update

RUN apt-get install -y --no-install-recommends curl nodejs libgmp-dev libmpfr-dev libmpc-dev

# Use official debian mirror
RUN echo "deb http://deb.debian.org/debian testing main" > /etc/apt/sources.list

RUN apt-get update

# For Security
RUN apt-get update && apt-get install -y --no-install-recommends zlib1g expat libldap-2.5-0 perl libsqlite3-0

RUN apt-get autoremove -y

RUN rm -rf /var/lib/apt/lists/*

# Copy Python environment and packages
ENV VIRTUAL_ENV=/app/api/.venv
COPY --from=packages ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Download nltk data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Copy source code
COPY . /app/api/

# Copy entrypoint
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ARG COMMIT_SHA
ENV COMMIT_SHA=${COMMIT_SHA}

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
