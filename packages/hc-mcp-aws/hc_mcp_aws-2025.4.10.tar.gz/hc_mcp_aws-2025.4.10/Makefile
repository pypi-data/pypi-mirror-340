# 
# This Makefile publishes your mcp server to our AWS CodeArtifact repository.
#
#

PYTHON_VERSION = 3.10
MCP_SERVER = $(shell grep -o 'name = "[^"]*"' pyproject.toml | cut -d'"' -f2)

### No changes below this line should be necessary

help:
	@echo "Package: $(MCP_SERVER)"
	@echo "Make targets:"
	@grep '^[^#[:space:]].*:' Makefile | cut -f1 -d: | xargs -n1 echo ' - '

new-version:
	@if [ -z "$(version)" ]; then \
		CURRENT_VERSION=$$(grep -o '"[0-9]*\.[0-9]*\.[0-9]*"' pyproject.toml | tr -d '"'); \
		MAJOR=$$(echo $$CURRENT_VERSION | cut -d. -f1); \
		MINOR=$$(echo $$CURRENT_VERSION | cut -d. -f2); \
		PATCH=$$(echo $$CURRENT_VERSION | cut -d. -f3); \
		NEW_PATCH=$$((PATCH + 1)); \
		version="$$MAJOR.$$MINOR.$$NEW_PATCH"; \
	fi; \
	echo "Updating to version $$version"; \
	sed -i 's/version = "[0-9]*\.[0-9]*\.[0-9]*"/version = "'$$version'"/' pyproject.toml
	@echo "Version updated to $$version in pyproject.toml"
	@echo "Version will be available at runtime via package metadata"
	@echo "Don't forget to commit the changes and create a tag"

prepare:
	@echo 'Preparing'
	@command -v uv > /dev/null || pip install uv
	@aws codeartifact login --tool pip --repository hctools --domain hc --domain-owner 256928933720 --region eu-west-1 
	@uvx --python $(PYTHON_VERSION) pip install build -qq
	@uvx --python $(PYTHON_VERSION) pip install twine -qq

build: prepare
	@echo 'Building'
	@uvx --python $(PYTHON_VERSION) --from build pyproject-build

publish: clean build
	@echo 'Uploading'
	@aws codeartifact login --tool twine --repository hctools --domain hc --domain-owner 256928933720 --region eu-west-1 && \
	export TWINE_USERNAME=aws && \
	export TWINE_PASSWORD=`aws codeartifact get-authorization-token --domain hc --domain-owner 256928933720 --query authorizationToken --output text` && \
	export TWINE_REPOSITORY_URL=`aws codeartifact get-repository-endpoint --domain hc --domain-owner 256928933720 --repository hctools --format pypi --query repositoryEndpoint --output text` && \
	uvx --python $(PYTHON_VERSION) twine upload dist/* 

publish-pypi: clean build
	@echo 'Uploading'
	@uvx --python $(PYTHON_VERSION) twine upload dist/* 

clean::
	@echo 'Cleaning'
	@rm -rf dist
	@rm -rf src/*.egg-info
	@rm -rf src/*/__pycache__
	@rm -rf .venv
