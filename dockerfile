FROM python:3.10.5-buster

COPY . /app

WORKDIR /app
# this is so opencv-python works
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN ls
RUN pip install -r requirements.txt
RUN pip install -e .

CMD python /app/bin/run_app.py -c /config/zenserver.json -d