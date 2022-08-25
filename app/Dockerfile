FROM python:3.10-slim as base
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
WORKDIR /app
COPY . /app
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

FROM base as tests
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN python -m pip install --no-cache-dir -U \
    mypy \
    flake8
WORKDIR /app
USER appuser
CMD ["bash", "run.sh"]

FROM base as build
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
USER appuser
CMD ["python", "run.py"]