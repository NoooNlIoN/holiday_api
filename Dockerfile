
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir -r requirements.lock


CMD  alembic upgrade head &&  uvicorn main:app --host 0.0.0.0 --port 8000 
