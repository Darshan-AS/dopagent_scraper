MODULE := scraper
BLUE = \033[0;34m
NC = \033[0m # No Color

define USAGE
Build system for ${BLUE}dopagent_scraper${NC}⚙️

Commands:
	${BLUE}init${NC}      Install Python dependencies with poetry
	${BLUE}lint${NC}      Run linters
	${BLUE}serve${NC}     Run app in dev environment
	${BLUE}clean${NC}     Remove logs and tmp files
endef

export USAGE
help:
	@echo "$$USAGE"

init:
	@echo "${BLUE}Installing poetry...${NC}\n"
	@pip install poetry
	@echo "${BLUE}Installing dependencies using poetry...${NC}\n"
	@poetry install --no-root

lint:
	@echo "${BLUE}Running Pylint against source and test files...${NC}\n"
	@poetry run pylint --rcfile=setup.cfg **/*.py
	@echo "${BLUE}Running Flake8 against source and test files...${NC}\n"
	@poetry run flake8
	@echo "${BLUE}Running Bandit against source files...${NC}\n"
	@poetry run bandit -r --ini setup.cfg

serve:
	@echo "${BLUE}Starting server at port 9080${NC}\n"
	@poetry run scrapyrt

clean:
	@echo "${BLUE}Removing logs and tmp files...${NC}\n"
	@rm -rf logs

.PHONY: help init lint serve clean
