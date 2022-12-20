FROM windpioneers/gdal-python:little-gecko-gdal-2.4.1-python-3.9-slim

# Set the application root directory (using a different base so we have to repeat this)
ENV PROJECT_ROOT=/workspace
WORKDIR $PROJECT_ROOT

# Install poetry and dependencies
ENV POETRY_HOME=/root/.poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH "$POETRY_HOME/bin:$PATH"
RUN poetry config virtualenvs.create false

# Service must listen to $PORT environment variable
ENV PORT 8000

# Ensure print statements and log messages promptly appear in Cloud Logging.
ENV PYTHONUNBUFFERED TRUE

# Install python dependencies - utilise layer caching for quick rebuilds
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-ansi --no-root --no-interaction --no-cache

# Copy local code to the application root directory
COPY . .

# Already installed dependencies, now install local packages
RUN poetry install

EXPOSE $PORT

ENV USE_OCTUE_LOG_HANDLER=1
ENV COMPUTE_PROVIDER=GOOGLE_CLOUD_RUN

ARG GUNICORN_WORKERS=1
ENV GUNICORN_WORKERS=$GUNICORN_WORKERS

ARG GUNICORN_THREADS=8
ENV GUNICORN_THREADS=$GUNICORN_THREADS

# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers $GUNICORN_WORKERS --threads $GUNICORN_THREADS --timeout 0 octue.cloud.deployment.google.cloud_run.flask_app:app
