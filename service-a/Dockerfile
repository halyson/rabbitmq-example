FROM python:3.8-alpine

RUN pip install pika

WORKDIR /app

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
