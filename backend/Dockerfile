FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3 pip libgl1 libglib2.0-0 && apt install -y curl

# install dependencies first
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN mim install mmcv-full

# Fix timezone issue
ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# copy all scripts
COPY . /app

ENTRYPOINT ["uvicorn", "main:app", "--port", "5000", "--host", "0.0.0.0"]

