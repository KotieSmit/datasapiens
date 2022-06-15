# FROM python:3.8
FROM mcr.microsoft.com/playwright/python

ARG WORK_DIR=/automated_tests

WORKDIR $WORK_DIR
COPY . .
RUN pip install -r requirements.txt 

ENTRYPOINT ["tail", "-f", "/dev/null"]
