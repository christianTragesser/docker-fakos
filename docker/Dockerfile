FROM python:3-alpine

COPY *.py /opt/

RUN pip install requests prometheus-client \
    kubernetes==6.0.0 python-json-logger --no-cache-dir && \
    addgroup -S -g 2222 fakos && \
    adduser -S -u 2222 -g fakos fakos && \
    chmod 755 /opt/*
USER fakos

ENV INTERVAL 10

EXPOSE 8000

CMD ["python", "/opt/fakos.py"]
