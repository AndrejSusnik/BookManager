FROM python:3.10.0-alpine

WORKDIR /app

ADD src/BookManagerService/ /app
ADD src/Config/config_managment.py /app

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "BookManagerService.py"]
