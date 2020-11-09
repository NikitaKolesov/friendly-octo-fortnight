FROM python:3.8

RUN pip install --no-cache-dir mysql-connector-python retrying

ARG VERSION=1

COPY filler.py /code/filler.py

CMD ["python", "/code/filler.py"]
