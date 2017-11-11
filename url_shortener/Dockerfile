FROM python:3.6
MAINTAINER Adrien Duffy <adrien.duffy@gmail.com>


RUN mkdir -p /app/url_shortener

WORKDIR /app/url_shortener

COPY requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY run.py .
COPY . url_shortener

CMD ["python", "run.py"]
