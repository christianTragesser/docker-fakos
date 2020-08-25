FROM python:3-alpine

RUN apk -U add gcc musl-dev python3-dev libffi-dev openssl-dev --no-cache && \
    pip install --upgrade pip --no-cache-dir && \
    pip install requests prometheus-client \
    kubernetes python-json-logger --no-cache-dir && \
    addgroup -S -g 2222 fakos && \
    adduser -S -u 2222 -g fakos fakos

COPY fakos /opt/fakos

RUN chmod 755 /opt/fakos/*

USER fakos

EXPOSE 8000

CMD ["/bin/sh", "-c", "cd /opt && python -m fakos"]