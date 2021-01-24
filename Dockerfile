FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /awsdescribe
WORKDIR /awsdescribe
COPY ./src/ /awsdescribe/
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000
