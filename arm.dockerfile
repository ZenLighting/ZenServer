FROM arm32v7/python:3.8.6-alpine

COPY . /app

WORKDIR /app
RUN ls
RUN pip install flask
RUN pip install paho-mqtt
RUN pip install dataclasses-json
RUN pip install .

EXPOSE 5000

CMD python /app/app.py