# syntax=docker/dockerfile:1

FROM python

WORKDIR /app

COPY ./src/result_generator/requirements.txt requirements.txt
COPY ./src/result_generator/result_generator.py result_generator.py
RUN pip3 install -r requirements.txt

CMD ["python", "result_generator.py"]