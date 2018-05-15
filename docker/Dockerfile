FROM python:2.7-alpine

COPY requirements.txt /opt/requirements.txt

COPY *.py /opt/

RUN pip install -r /opt/requirements.txt && \
    addgroup -S -g 2222 fakos && \
    adduser -S -u 2222 -g fakos fakos && \
    chmod 777 /opt/*
USER fakos

EXPOSE 8000

CMD ["python", "/opt/fakos.py"]
