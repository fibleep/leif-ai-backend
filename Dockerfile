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
COPY .. .

# Installing project dependencies
RUN poetry install --only main

# Cleaning up unnecessary packages and clearing cache
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache


EXPOSE 8000
## Create a .env
#CMD ["touch", ".env"]
#RUN echo "BACKEND_RELOAD=True" >> .env \
#    && echo "BACKEND_DB_HOST=$BACKEND_DB_HOST" >> .env \
#    && echo "BACKEND_SUPABASE_SERVICE_ROLE=$BACKEND_SUPABASE_SERVICE_ROLE" >> .env \
#    && echo "BACKEND_SUPABASE_PUBLIC_API=$BACKEND_SUPABASE_PUBLIC_API" >> .env \
#    && echo "BACKEND_OPENAI_API_KEY=$BACKEND_OPENAI_API_KEY" >> .env \
#    && echo "BACKEND_DB_PASSWORD=$BACKEND_DB_PASSWORD" >> .env \
#    && echo "BACKEND_SECRET_KEY=$BACKEND_SECRET_KEY" >> .env \
#    && echo "BACKEND_ALGORITHM=$BACKEND_ALGORITHM" >> .env \
#    && echo "DB_URL=$DB_URL" >> .env \
#    && echo "BACKEND_SUPABASE_URL=$BACKEND_SUPABASE_URL" >> .env \
#    && echo "BACKEND_COHERE_API_KEY=$BACKEND_COHERE_API_KEY" >> .env \
CMD ["poetry", "run", "python", "-m", "backend"]
