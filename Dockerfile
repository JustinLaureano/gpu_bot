FROM python:latest

ENV PYTHONUNBUFFERED=1

# Default to local timezone
ENV TZ=America/Detroit
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set  up cron
RUN apt-get -y update && apt-get -y install cron nano
COPY cron/archive_logs /etc/cron.d/archive_logs
RUN crontab /etc/cron.d/archive_logs

# Set up project directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# Install package requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Start the bot when the container starts
CMD [ "python", "./main.py"]
