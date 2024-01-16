FROM python:3.10.0-alpine

WORKDIR /app

ADD src/BookInfoRetrievalService/ /app
ADD src/Config/ /app

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "BookInfoRetrievalService.py"]
