FROM python:3.11

RUN apt-get update -y && \
    apt install libpq-dev -y

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "main.py" ]