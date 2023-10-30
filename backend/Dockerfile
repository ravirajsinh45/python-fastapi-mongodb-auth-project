FROM python:3.11.4

RUN mkdir /usr/app
COPY . /usr/app
WORKDIR /usr/app
RUN apt-get update

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
