FROM python:3.9-slim-buster
WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "app:app", "-b localhost:5000"]