# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app/

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Fix timezone issue
ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["python", "result_generator.py"]