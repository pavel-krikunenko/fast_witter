FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ=Etc/UTC

WORKDIR /code
COPY . /code
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
     && echo $TZ > /etc/timezone \
     && apt update \
     && apt install -y --assume-yes python3-dev \
        libpq-dev \
        build-essential \
        python3-pip \
     && pip3 install -r requirements.txt

CMD uvicorn main:app --port 8010 --host 0.0.0.0 --reload
