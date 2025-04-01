FROM python:3.12-slim

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8077"]