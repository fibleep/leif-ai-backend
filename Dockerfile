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
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache

EXPOSE 8000

# Set environment variables
ENV BACKEND_RELOAD=True \
    BACKEND_DB_HOST=$backend-db-host \
    BACKEND_SUPABASE_SERVICE_ROLE=$backend-sb-sr \
    BACKEND_SUPABASE_PUBLIC_API=$backend-sb-api \
    BACKEND_OPENAI_API_KEY=$backend-openai-key \
    BACKEND_DB_PASSWORD=$backend-db-password \
    BACKEND_SECRET_KEY=$backend-secret-key \
    BACKEND_ALGORITHM=$backend-algorithm \
    DB_URL=$db-url \
    BACKEND_SUPABASE_URL=$backend-sb-url \
    BACKEND_COHERE_API_KEY=$backend-cohere-key

CMD ["poetry", "run", "python", "-m", "backend"]
