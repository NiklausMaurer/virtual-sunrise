FROM python:3.10-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY main.py .
COPY sunrise ./sunrise

CMD ["python3", "/app/main.py"]
