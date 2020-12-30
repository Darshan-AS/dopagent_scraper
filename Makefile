MODULE := scraper

# Define standard colors
BLACK		:= $(shell tput setaf 0)
RED			:= $(shell tput setaf 1)
GREEN		:= $(shell tput setaf 2)
YELLOW		:= $(shell tput setaf 3)
BLUE		:= $(shell tput setaf 4)
MAGENTA		:= $(shell tput setaf 5)
CYAN		:= $(shell tput setaf 6)
WHITE		:= $(shell tput setaf 7)

# Define standard text effects
BOLD		:= $(shell tput bold)
UNDERLINE	:= $(shell tput smul)
BLINK		:= $(shell tput blink)
INVISIBLE	:= $(shell tput invis)

# Reset all options
RESET		:= $(shell tput sgr0)

# set target color
COLOR		:= $(BLUE)

define USAGE
Build system for ${BLUE}dopagent_scraper${RESET}

${BOLD}Commands${RESET}:
  ${COLOR}init${RESET}		Install Python dependencies with poetry
  ${COLOR}format${RESET}	Format code
  ${COLOR}lint${RESET}		Run linters
  ${COLOR}run${RESET}		Run app in dev environment
  ${COLOR}clean${RESET}		Remove logs, cache and tmp files
endef

export USAGE
help:
	@echo "$$USAGE"

init:
	@echo "${COLOR}Installing poetry...${RESET}"
	@pip install poetry
	@echo "${COLOR}Installing dependencies using poetry...${RESET}"
	@poetry install --no-root

format:
	@echo "${COLOR}Running black formatter against source and test files...${RESET}"
	@echo "Fixing your spaghetti code..."
	@poetry run black .

lint:
	@echo "${COLOR}Running Bandit against source files...${RESET}"
	@poetry run bandit -r --ini setup.cfg
	@echo "${COLOR}Running Pylint against source and test files...${RESET}"
	@poetry run pylint --rcfile=setup.cfg **/*.py
	@echo "${COLOR}Running Flake8 against source and test files...${RESET}"
	@poetry run flake8

run:
	@echo "${COLOR}Starting server...${RESET}"
	@echo "or Skynet... You never know!"
	@poetry run scrapyrt -i 0.0.0.0

clean:
	@echo "${COLOR}Removing pycache...${RESET}"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@echo "${COLOR}Deleting logs...${RESET}"
	@rm -rf logs
	@echo "${COLOR}Cleaning up tmp files and cache...${RESET}"
	@rm -rf logs accounts reports
	@echo "${COLOR}Deleting Space...${RESET}"
	@echo "${COLOR}Deleting Time...${RESET}"
	@echo "${COLOR}Deleting the Universe...${RESET}"
	@echo "Cleaned!"

.PHONY: help init format lint run clean
