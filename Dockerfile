FROM --platform=linux/amd64 python:3.11.4-slim-bullseye

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \
    libsm6 \
    libxext6

# Install poetry
RUN pip install poetry

# Copying project files
COPY .. .

# Cleaning up unnecessary packages and clearing cache
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache \

RUN poetry config virtualenvs.create false
RUN --mount=type=cache,target=/root/.cache poetry install --only main


EXPOSE 80
RUN ls -la
CMD ["poetry", "run", "python", "-m", "backend"]
