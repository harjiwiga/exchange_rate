# Pull base image
FROM python:3.7-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Copy project
COPY . /code/

# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pip3 install psycopg2
RUN pip3 install -r requirements.txt
#COPY ./Pipfile /code/Pipfile
RUN pipenv install --deploy --system --skip-lock --dev

