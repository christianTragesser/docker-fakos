FROM python:2.7-alpine

ADD fakos.py /opt/fakos.py

RUN pip install kubernetes

CMD ["python", "/opt/fakos.py"]
