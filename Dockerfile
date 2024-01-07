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
# Create a .env
RUN touch .env \
    && echo "BACKEND_RELOAD=True" >> .env \
    && echo "BACKEND_DB_HOST=$backend-db-host" >> .env \
    && echo "BACKEND_SUPABASE_SERVICE_ROLE=$backend-sb-sr" >> .env \
    && echo "BACKEND_SUPABASE_PUBLIC_API=$backend-sb-api" >> .env \
    && echo "BACKEND_OPENAI_API_KEY=$backend-openai-key" >> .env \
    && echo "BACKEND_DB_PASSWORD=$backend-db-password" >> .env \
    && echo "BACKEND_SECRET_KEY=$backend-secret-key" >> .env \
    && echo "BACKEND_ALGORITHM=$backend-algorithm" >> .env \
    && echo "DB_URL=$db-url" >> .env \
    && echo "BACKEND_SUPABASE_URL=$backend-sb-url" >> .env \
    && echo "BACKEND_COHERE_API_KEY=$backend-cohere-key" >> .env \

CMD ["poetry", "run", "python", "-m", "backend"]
