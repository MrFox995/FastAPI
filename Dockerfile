FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

COPY . .

# OLD: CMD [ "uvicorn", "app.mainORM:app", "--host", "0.0.0.0", "--port", "8000" ]
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]