FROM python:3.7-alpine

WORKDIR /app

RUN pip install -U pipenv --no-cache-dir
COPY Pipfile Pipfile.lock ./

RUN pipenv install --clear --deploy --system
COPY . .
CMD ["python", "app.py"]
