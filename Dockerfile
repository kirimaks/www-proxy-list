FROM ubuntu:latest

RUN apt update && \
    apt install -y python3 python3-dev python3-pymongo python3-pip libssl-dev libffi-dev && \
    pip3 install --upgrade pip && pip3 install scrapy
    

COPY ["./", "/proxy_list"]
WORKDIR /proxy_list

CMD ["/usr/bin/python3", "run.py"]
