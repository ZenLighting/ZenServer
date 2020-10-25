FROM arm32v7/python:3.8.6-alpine

COPY . /app

RUN pip install -r requirements.txt
RUN pip install .

CMD python /app/app.py