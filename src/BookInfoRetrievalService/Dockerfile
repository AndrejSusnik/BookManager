FROM python:3.10.0-alpine

WORKDIR /app

ADD ./BookInfoRetrievalService.py /app
ADD ./requirements.txt /app

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "BookInfoRetrievalService.py"]
