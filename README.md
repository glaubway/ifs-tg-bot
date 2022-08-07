# Ingress FirstSatuday Telegram bot

## Description

TODO

## Features

TODO

## Installation

### Clone the repository to your local env.

```sh
git clone https://github.com/glaubway/ifs-tg-bot.git
```

### Edit the configuration file:

Then edit .env file with any text editors like vim, nano, mcedit, etc:

```sh
cd ifs-tg-bot
mv .env_sample .env
vim .env
```

Fill variables with your information:

```
BOT_TOKEN = ''          // your bot token
CHAT_ID = ''            // chat id with admins
GLOBAL_ADMINS = ''      // admins telegram nickname, "," as separator (without @)
EVENT_CITY = ''         // city name (Kyiv)
EVENT_TIMEZONE = ''     // your city timezone (Europe/Kiev)
EVENT_LANGUAGE = ''     // your event language (en or ua) 
```

### Start the bot

You should have installed docker packages.
```sh
docker compose up -d
```

## Libraries

The bot is currently extended with the following libraries.

| Plugin | Link |
| ------ | ------ |
| python-telegram-bot | [Github](https://github.com/python-telegram-bot/python-telegram-bot/) |

## License

GPL-3.0 license
