# base image
FROM python:3.11-slim-bullseye
RUN apt-get update && apt-get -y install libpq-dev gcc

# set environment variables
ENV PYTHONUNBUFFERED 1

# set directory
WORKDIR /app

# add application and install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY . ./

# run the program
CMD ["supervisord", "-c", "supervisord.conf"]
