FROM python:3.8

RUN pip install --no-cache-dir mysql-connector-python

COPY filler.py /code/filler.py

CMD ["python", "/code/filler.py"]