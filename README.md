# DOP Agent Scraper

A robust and scalable web scraper for the India Post DOP Agent portal (`https://dopagent.indiapost.gov.in`). This project provides tools to automate account detail extraction, installment management, and report generation.

## Features

- **Authentication**: Automated login and session management.
- **Account Scraping**: Fetch comprehensive details for specific accounts or the entire list.
- **Installment Automation**: Automate the process of saving and paying installments.
- **Report Generation**: Search and download transaction reports in PDF or XLS formats.
- **Real-time API**: Integrated with `scrapyrt` to provide an HTTP interface for running spiders.
- **Dockerized**: Ready-to-use Docker environment for easy deployment.

## Prerequisites

- **Python**: 3.9+
- **Poetry**: For dependency management.
- **Docker & Docker Compose**: (Optional) For running in a containerized environment.

## Getting Started

### 1. Installation

Initialize the project and install dependencies:

```bash
make init
```

### 2. Running the Project

#### Local Environment
Start the ScrapyRT server locally:

```bash
make run
```
The server will be available at `http://localhost:9080`.

#### Docker Environment
Bring up the project using Docker Compose:

```bash
make up
```

## Usage (Real-time API)

The project exposes an HTTP API via `scrapyrt`. You can interact with it using `curl` or any HTTP client.

### Authentication
Authenticate to get session-specific URLs (required for other spiders):

```bash
curl "http://localhost:9080/crawl.json?spider_name=auth&crawl_args={\"agent_id\":\"YOUR_ID\",\"password\":\"YOUR_PASSWORD\"}"
```

### Scraping Accounts
After getting the `accounts_url` from the auth spider:

```bash
# Scrape all accounts
curl "http://localhost:9080/crawl.json?spider_name=accounts&url=PASTE_ACCOUNTS_URL_HERE"

# Scrape specific accounts
curl "http://localhost:9080/crawl.json?spider_name=accounts&url=PASTE_ACCOUNTS_URL_HERE&crawl_args={\"account_numbers\":[\"1234567890\"]}"
```

### Downloading Reports
```bash
curl "http://localhost:9080/crawl.json?spider_name=reports&url=PASTE_REPORTS_URL_HERE&crawl_args={\"reference_number\":\"REF123456\"}"
```

## Development

### Available Commands (Makefile)

- `make init`: Install Python dependencies.
- `make format`: Format code using Black.
- `make lint`: Run linters (Bandit, Pylint, Flake8).
- `make run`: Run the server locally.
- `make up`: Run the server in Docker.
- `make down`: Stop Docker containers.
- `make clean`: Clean up logs and temporary files.

## Project Structure

- `scraper/spiders/`: Contains the logic for different scraping tasks (auth, accounts, installments, reports).
- `scraper/items/`: Defines the data structures for scraped data.
- `scraper/pipelines/`: Handles data storage and post-processing.
- `scraper/loaders/`: Logic for extracting and cleaning data from HTML.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
