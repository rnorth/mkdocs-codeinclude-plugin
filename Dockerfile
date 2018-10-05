FROM python:3.6.6-slim

RUN pip install mkdocs-material

COPY . /src
RUN pip install -e /src
EXPOSE 8000

CMD exec mkdocs serve --dev-addr 0.0.0.0:8000