FROM alpine:latest
RUN apk update &&\
apk add python3 &&\
pip3 install Flask &&\
pip3 install pika &&\
pip3 install requests &&\
pip3 install simplejson &&\
pip3 install docker
COPY worker.py /worker.py
