FROM ubuntu:22.04

WORKDIR /app


RUN apt-get update && apt-get install -y python3 pip libgl1 libglib2.0-0

# install dependencies first
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN mim install mmcv-full

# copy all scripts
COPY . /app

ENV FLASK_APP app
ENTRYPOINT ["python3", "-u", "-m", "flask", "run", "--host=0.0.0.0"]


