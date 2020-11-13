FROM python:3.8-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS build

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies to /.venv
COPY Pipfile Pipfile.lock ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

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
ENTRYPOINT ["scrapyrt", "-i", "0.0.0.0"]
EXPOSE 9080
