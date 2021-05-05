FROM python:3.6.13

ADD requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

COPY ./source /app/

WORKDIR /app

ENTRYPOINT ["python"]
