FROM python:3.8-buster as build

WORKDIR /opt/app

COPY requirements.lock /opt/app
RUN pip3 install --upgrade pip \
 && pip3 install -r requirements.lock

FROM python:3.8-slim-buster as runnner

COPY --from=build /usr/local/lib/python3.8/site-packages /root/.local/lib/python3.8/site-packages
COPY src /opt/app/slackbot

WORKDIR /opt/app/slackbot

ENTRYPOINT ["python", "run.py"]
