FROM python:2.7-alpine

COPY requirements.txt /opt/requirements.txt

RUN pip install -r /opt/requirements.txt

COPY *.py /opt/

EXPOSE 8000

CMD ["python", "/opt/fakos.py"]
