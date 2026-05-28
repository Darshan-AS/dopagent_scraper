FROM python:3.9-slim as base

# Turn off UI interaction
ENV DEBIAN_FRONTEND noninteractive

# Setup locales
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    && echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen && /usr/sbin/locale-gen \
    && rm -rf /var/lib/apt/lists/*

# Set ENV for locales, python, and pip
ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off

# Set project specific ENVs (APP_MODULE is for uvicorn)
ENV WORKING_PATH=/dopagent_scraper \
    APP_HOST=0.0.0.0 \
    APP_PORT=9080


FROM base AS build

# Install build tools
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${WORKING_PATH}

# Tell poetry to create venv in current directory and turn off UI
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

# Install poetry and build dependencies
RUN pip install --upgrade pip \
    && pip install "setuptools<58.0.0" "poetry<2.0.0" "wheel"

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
# We use a multi-step install to handle the legacy demjson package which requires 
# --no-build-isolation and a legacy setuptools version.
RUN poetry env use python \
    && poetry run pip install "setuptools<58.0.0" "wheel" \
    && poetry run pip install demjson==2.2.4 --no-build-isolation \
    && poetry install --no-root --no-dev

# Add venv to path
ENV PATH ${WORKING_PATH}/.venv/bin:$PATH


FROM build as dev

# Set default working directory
WORKDIR ${WORKING_PATH}

# Install project dependencies including dev
RUN poetry install --no-root

# Copy application into container. This is just a fallback. Use volumes to mount the source code
COPY . .

# Run the application
CMD scrapyrt -i ${APP_HOST} -p ${APP_PORT}
EXPOSE 9080


FROM base AS prod

# Create and switch to a new user
RUN useradd dopagent
USER dopagent

# Copy venv from build stage
COPY --from=build ${WORKING_PATH}/.venv ${WORKING_PATH}/.venv
ENV PATH ${WORKING_PATH}/.venv/bin:$PATH

# Set default working directory
WORKDIR ${WORKING_PATH}

# Copy application into container
COPY . .

# Run the application
ENTRYPOINT scrapyrt -i ${APP_HOST} -p ${APP_PORT}
EXPOSE 9080
