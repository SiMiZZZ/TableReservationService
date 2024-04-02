FROM python:3.12

RUN apt-get update \
	&& apt-get install -y --no-install-recommends

RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false --local
RUN poetry install
