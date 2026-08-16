# Base Image
FROM python:3.9-slim

# Base Rule
RUN adduser --disabled-password myuser
WORKDIR /app
COPY . .

# Requirements
RUN pip install Flask

# setting
ENV APP_VERSION=1.0

USER myuser
CMD ["python", "app.py"]
