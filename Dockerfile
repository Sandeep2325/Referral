FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /referral
WORKDIR /referral
COPY . /referral/
RUN pip install -r requirements.txt

