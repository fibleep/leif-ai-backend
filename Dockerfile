FROM python:3.11.4-slim-bullseye
RUN apt-get update && apt-get install -y \
  gcc

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.4.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY . .

# Installing requirements
RUN poetry install --only main
# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*


EXPOSE 8000
CMD ["ls", "-la"]
CMD ["poetry", "run", "python", "-m", "backend"]
