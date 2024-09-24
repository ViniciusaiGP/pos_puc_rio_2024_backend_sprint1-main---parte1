FROM python:3.9.10-slim-buster

WORKDIR /
COPY ./requirements.txt /
RUN apt-get update && apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
COPY . / 
CMD ["python", "app.py"]
