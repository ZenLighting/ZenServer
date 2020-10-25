FROM python:3.8.6-alpine3.12

COPY . /app

WORKDIR /app
RUN ls
RUN pip install -r requirements.txt
RUN pip install .

EXPOSE 5000

CMD python /app/app.py