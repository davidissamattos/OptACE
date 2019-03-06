FROM python:3.7
LABEL maintainer="issamattos.david@gmail.com"

COPY . /src/optace-backend
WORKDIR /src/optace-backend

RUN pip install -r requirements.txt


EXPOSE 8081
ENTRYPOINT ["gunicorn", "main:app"]
#ENTRYPOINT ["python", "./main.py"]