FROM python:3-alpine

COPY *.py /opt/

RUN apk -U add gcc musl-dev python3-dev libffi-dev openssl-dev --no-cache && \
    pip install --upgrade pip --no-cache-dir && \
    pip install requests prometheus-client \
    kubernetes python-json-logger --no-cache-dir && \
    addgroup -S -g 2222 fakos && \
    adduser -S -u 2222 -g fakos fakos && \
    chmod 755 /opt/*
USER fakos

ENV INTERVAL 10

EXPOSE 8000

CMD ["/bin/sh", "-c", "python -u /opt/fakos"]