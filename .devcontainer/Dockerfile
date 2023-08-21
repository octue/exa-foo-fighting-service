FROM windpioneers/gdal-python:little-gecko-gdal-2.4.1-python-3.9-dev

# Tell zsh where you want to store history
ENV HISTFILE="/workspaces/exa-foo-fighting-service/.devcontainer/.zsh_history"

# Install poetry
USER vscode
ENV POETRY_HOME=/home/vscode/.poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH "$POETRY_HOME/bin:$PATH"
RUN poetry config virtualenvs.create false

# Cache the poetry dependencies
#   Note: Use --no-root install as there's no source code copied into the image yet
#   Note: Use --no-cache option to make it explicit that poetry has no cache (this layer creates the cache)
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-ansi --no-root --no-interaction --no-cache

