FROM python:3.12-slim


WORKDIR /src


COPY requirements.txt .
COPY ./server /src/server

RUN pip install --no-cache-dir --requirement requirements.txt

ENV PYTHONPATH=/src/server

ENTRYPOINT ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]