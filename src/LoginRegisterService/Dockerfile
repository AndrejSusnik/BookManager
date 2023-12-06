FROM python:3.10.0-alpine

RUN mkdir /app

WORKDIR /app

ADD ./LoginRegisterService.py /app
ADD ./requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 5002

CMD ["python", "LoginRegisterService.py"]