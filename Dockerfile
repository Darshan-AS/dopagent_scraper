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


FROM base AS build

# Set ENV for poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install gcc and git
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Get poetry and install python dependencies to /.venv
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install --no-root --no-dev


FROM base AS runtime

# Install make
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy venv from build stage
COPY --from=build /.venv /.venv
ENV PATH /.venv/bin:$PATH

# Create and switch to a new user
RUN useradd --create-home dopagent
WORKDIR /home/dopagent
USER dopagent

# Copy application into container
COPY . .

# Run the application
ENTRYPOINT ["make"]
EXPOSE 9080
