# GPU Bot

A simple bot to notify me when a gpu comes in stock from Best Buy

## Setup

Create an environment file and fill in the values appropriately

```bash
cp src/.env.example src/.env
```

`GMAIL_ADDRESS` and `GMAIL_PASSWORD` - Gmail account that will be sending the emails

`NOTIFICATION_ADDRESS` - Email account that will receiving the in stock notifications

`BESTBUY_URL` - The Best Buy URL to check if GPU's are in stock

`CHECK_STATUS_INTERVAL` - How often the bot should check the in stock availability

## Run

run the following command to start the bot

```bash
docker-compose up -d
```

## Stop

run the following to stop the bot

```bash
docker-compose down
```

## Prerequisites

Docker installed on machine