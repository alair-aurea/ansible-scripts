FROM python:2.7-alpine3.8

RUN ["mkdir", "/home/ansible"]
WORKDIR /home/ansible
RUN ["apk", "add", "--no-cache", "ansible"]
RUN ["apk", "add", "--no-cache", "openssh-client"]
RUN ["apk", "add", "--no-cache", "git"]
RUN ["git", "clone", "https://github.com/alair-aurea/ansible-scripts.git"]
WORKDIR /home/ansible/ansible-scripts
RUN ["pip", "install", "-r", "requirements.txt"]
CMD python run.py
