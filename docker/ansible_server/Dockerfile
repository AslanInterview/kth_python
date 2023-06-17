FROM willhallonline/ansible:latest

RUN mkdir /root/demo

WORKDIR /root/demo

COPY src/* .
COPY src/roles .


RUN pip3 install -r /root/demo/requirements.txt
