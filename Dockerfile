FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .
WORKDIR /usr/src/app/src
CMD [ "uvicorn","main:api" ,"--host","0.0.0.0","--port","8000"]