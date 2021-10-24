FROM python:3.9.2-buster


RUN apt-get update && apt-get install -y cron && apt-get install -y liblzma-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir uvicorn

COPY update_cron.sh /etc/cron.d/update_cron.sh

RUN ["chmod", "0644", "/etc/cron.d/update_cron.sh"]

RUN crontab /etc/cron.d/update_cron.sh

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./docker-entrypoint.sh /entrypoint/docker-entrypoint.sh
COPY . .

RUN ["chmod", "+x", "docker-entrypoint.sh"]
ENTRYPOINT ["/entrypoint/docker-entrypoint.sh"]
CMD python main.py

