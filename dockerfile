FROM python:3.10.5-buster

COPY . /app

WORKDIR /app
RUN ls
RUN pip install -r requirements.txt
RUN pip install -e .

CMD python /app/bin/run_app.py -c /config/zenserver.json -d