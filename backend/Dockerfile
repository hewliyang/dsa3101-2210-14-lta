FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3 pip libgl1 libglib2.0-0

# install dependencies first
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN mim install mmcv-full

# copy all scripts
COPY . /app

ENTRYPOINT ["uvicorn", "main:app", "--port", "5000", "--host", "0.0.0.0"]

