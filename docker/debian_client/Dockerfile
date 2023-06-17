FROM debian:bookworm-slim
FROM python:3.10-bookworm

RUN apt update && apt install openssh-server -y

RUN echo "\nPermitRootLogin yes" >> /etc/ssh/sshd_config

RUN echo "root:Docker!" | chpasswd 

RUN echo "service ssh restart"