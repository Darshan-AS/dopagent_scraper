FROM python:3.8-slim

ENV DEBIAN_FRONTEND noninteractive
ENV PROJECT_DIR /dopagent_scraper

WORKDIR ${PROJECT_DIR}

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install gcc && \
    apt-get -y install git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
RUN pipenv install --system --deploy --clear

COPY . ${PROJECT_DIR}/

ENTRYPOINT ["scrapyrt", "-i", "0.0.0.0"]
EXPOSE 9080
