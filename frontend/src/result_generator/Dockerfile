# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app/

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python", "result_generator.py", "--host=0.0.0.0"]