FROM python:3.10.0-alpine

WORKDIR /app

ADD src/OpenAPI/ /app

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5003

CMD ["python", "main.py"]