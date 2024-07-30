FROM python:3.12.2-slim

WORKDIR /flask_app_docker 

COPY requirements.txt .

RUN apt-get update && \
    pip3 install -r requirements.txt --no-cache-dir

COPY /app .

# RUN python3 init_db.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
