SHELL := /bin/bash

OPENAI_MODEL ?= gpt-4o-mini

.PHONY: install smoke push-private push-public pull

install:
	uv sync

# Minimal smoke test: saves a dataset (-s). Results are written under the env's
# own outputs/evals directory (e.g., environments/<env>/outputs/evals/... ).
.PHONY: smoke
SMOKE_ENV ?= vb-wordle-proxy
SMOKE_NUM ?= 1
SMOKE_R ?= 1
smoke:
	set -a; [ -f .env ] && source .env; set +a; \
	uv run vf-eval $(SMOKE_ENV) \
	  -m $${OPENAI_MODEL:-$(OPENAI_MODEL)} \
	  -n $${NUM_EXAMPLES:-$(SMOKE_NUM)} \
	  -r $${ROLLOUTS_PER_EXAMPLE:-$(SMOKE_R)} \
	  -s -k OPENAI_API_KEY

# Push an environment in environments/<env_id with hyphens converted to underscores>
# Requires: ENV_ID
push-private:
	@:$(if $(ENV_ID),,$(error ENV_ID is required, e.g., make push-private ENV_ID=vb-wordle-proxy))
	cd environments/$(subst -,_,$(ENV_ID)) && prime env push --visibility PRIVATE

push-public:
	@:$(if $(ENV_ID),,$(error ENV_ID is required, e.g., make push-public ENV_ID=vb-wordle-proxy))
	cd environments/$(subst -,_,$(ENV_ID)) && prime env push --visibility PUBLIC

# Pull an environment's source into a local folder (defaults target to environments/)
# Requires: ENV_SLUG (owner/name or owner/name@version)
TARGET ?= environments
pull:
	@:$(if $(ENV_SLUG),,$(error ENV_SLUG is required, e.g., make pull ENV_SLUG=will/wordle))
	mkdir -p $(TARGET)
	prime env pull $(ENV_SLUG) --target $(TARGET)
