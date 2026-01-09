FROM python:3.11-slim

RUN pip install poetry
RUN poetry config virtualenvs.create false

ARG VERSION

ENV LANG="en_US.UTF-8"
ENV VERSION_NUMBER=$VERSION

WORKDIR /src
COPY . .

RUN poetry install --no-interaction --no-ansi

ENTRYPOINT ["poetry", "run", "ai-news-feed"]
