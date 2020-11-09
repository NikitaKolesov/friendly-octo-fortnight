FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install flask mysql-connector-python retrying
ARG VERSION=1
COPY app.py .
CMD ["flask", "run"]
