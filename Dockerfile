FROM python:3.9.7

WORKDIR /app/

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y netcat

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry install

COPY ./app /app
COPY ./app/entrypoint.sh /app

ENTRYPOINT ["/app/entrypoint.sh"]