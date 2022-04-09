FROM python:3.8.5

WORKDIR /code

COPY backend/foodgram/requirements.txt .

RUN pip3 install -r requirements.txt

COPY backend/foodgram/ .

CMD ['gunicorn', 'foodgram.wsgi:application', '--bind', '0.0.0.0:8000']
