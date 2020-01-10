FROM alpine:latest
RUN apk update &&\
apk add python3 &&\
pip3 install requests &&\
pip3 install simplejson
COPY worker.py /worker.py
