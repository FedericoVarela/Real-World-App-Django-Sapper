FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app

COPY ./.env ./server/requirements.txt ./

RUN pip install --upgrade pip \
    && pip3 install -r requirements.txt && \
    chmod +x ./docker/entrypoint.sh
    
COPY ./server .

ENTRYPOINT [ "./docker/entrypoint.sh" ]

