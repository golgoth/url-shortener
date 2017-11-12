FROM python:3.6
MAINTAINER Adrien Duffy <adrien.duffy@gmail.com>

RUN mkdir -p /app/integration_test

WORKDIR /app/integration_test

COPY requirements-it-test.txt .

RUN pip install --no-cache-dir -r ./requirements-it-test.txt

COPY integration_test.py .

CMD ["python", "integration_test.py"]
