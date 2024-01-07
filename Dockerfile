FROM python:3.11.4-slim-bullseye

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \
    libsm6 \
    libxext6

# Install poetry
RUN pip install poetry

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying project files
COPY . .

# Installing project dependencies
RUN poetry install --only main

# Cleaning up unnecessary packages and clearing cache
RUN apt-get purge -y gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "backend"]
