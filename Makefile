# SQL Sheet — everyday commands.  Run `make` to see them all.
#
#   make install      create venv/ and install the dependencies
#   make results      after changing a lesson: work out its expected results on PostgreSQL
#   make run          start the server with auto-reload
#   make deploy       check, then push to GitHub (Render deploys from there)

PORT   ?= 8001
VENV   ?= venv
PYTHON ?= $(VENV)/bin/python
UVICORN = $(VENV)/bin/uvicorn
BRANCH ?= main
URL     = http://127.0.0.1:$(PORT)

.DEFAULT_GOAL := help
.PHONY: help install results run run-lan start open check clean deploy deploy-hook status

help: ## Show this list
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  \033[32mmake %-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "  Options: PORT=8002 make run   ·   RENDER_DEPLOY_HOOK=<url> make deploy-hook"

install: ## Create venv/ and install requirements.txt
	test -d $(VENV) || python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	npm install

results: ## After changing a lesson: run its SQL on PostgreSQL and save course_results.json (needs Node)
	@$(PYTHON) scripts/build_results.py

run: ## Start locally with auto-reload (port 8001, change with PORT=…)
	$(UVICORN) main:app --reload --port $(PORT)

run-lan: ## Start for other computers on your network (collaboration)
	@echo "Others open: http://$$(ipconfig getifaddr en0 2>/dev/null || hostname -I 2>/dev/null | cut -d' ' -f1):$(PORT)/"
	$(UVICORN) main:app --reload --host 0.0.0.0 --port $(PORT)

start: ## Start like Render does (no reload)
	$(UVICORN) main:app --host 0.0.0.0 --port $(PORT)

open: ## Open the trainer and the lessons page in the browser
	open $(URL)/ 2>/dev/null || xdg-open $(URL)/
	open $(URL)/lessons 2>/dev/null || xdg-open $(URL)/lessons

check: ## Check the code, the lessons and that course_results.json is up to date
	@echo "Checking…"
	@python3 scripts/check.py

clean: ## Remove Python caches
	find . -name "__pycache__" -not -path "./$(VENV)/*" -type d -prune -exec rm -rf {} +

deploy: check ## Check, then push to GitHub; Render deploys automatically
	@if [ -n "$$(git status --porcelain)" ]; then \
	  echo "You have uncommitted changes. Commit them first:"; git status --short; exit 1; \
	fi
	git push origin $(BRANCH)
	@echo "Pushed. Render picks it up in a minute: watch the Events tab of the sql-sheet service."

deploy-hook: ## Ask Render to redeploy now (needs RENDER_DEPLOY_HOOK)
	@test -n "$(RENDER_DEPLOY_HOOK)" || (echo "Set RENDER_DEPLOY_HOOK to the Deploy Hook URL from Render → Settings."; exit 1)
	curl -fsS -X POST "$(RENDER_DEPLOY_HOOK)" && echo "Deploy started."

status: ## Show git status and what is not pushed yet
	@git status --short --branch
	@echo "Not pushed:"; git log --oneline origin/$(BRANCH)..HEAD 2>/dev/null || echo "  (no remote branch yet)"
