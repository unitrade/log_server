FROM python:3.7-alpine

WORKDIR /app
COPY . .
RUN pip install -U pipenv --no-cache-dir \
    && pipenv install --clear --deploy --system

CMD ["python", "app.py"]
