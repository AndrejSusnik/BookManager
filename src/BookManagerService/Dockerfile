FROM python:3.10.0-alpine

RUN mkdir /app

WORKDIR /app

ADD ./BookManagerService.py /app
ADD ./requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "BookManagerService.py"]