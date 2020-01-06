FROM alpine:latest
RUN apk update && apk add python3
ADD worker.py /home/
