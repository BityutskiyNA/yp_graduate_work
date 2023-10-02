FROM python:3.10
RUN apt-get update && apt-get -y install cron
WORKDIR /app
COPY script.sh .
RUN echo "* * * * * root /bin/bash /app/script.sh" >> /etc/cron.d/mycron
RUN chmod +x /app/script.sh
CMD cron && tail -f /var/log/cron.log