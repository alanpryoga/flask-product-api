FROM python:3.9.15-alpine3.17

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080

CMD [ "python", "app.py" ]
