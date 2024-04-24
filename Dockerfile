FROM python:3.10-slim-buster

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt \
    && pip install django

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/django/django.git

COPY . /app

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["index.py"]