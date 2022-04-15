# pull official base image
FROM python:3.8

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip3 install --upgrade pip
RUN apt-get update
# RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
COPY . /app
