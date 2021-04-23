FROM python:3.7-alpine

WORKDIR /app

RUN pip install -U pipenv
COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system
COPY . .
CMD ["python", "app.py"]
