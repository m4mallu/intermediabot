# [IntermediaBot](https://github.com/m4mallu/intermediabot) 🤖

An Open Source ALL-In-One Telegram RoBot, that can do a lot of things.


# About :
A advanced telegram bot which performs the following functions differently.

- File renaming 
- Converting to video
- Extracting screenshots 
- Trimming streams
- Downloading TouTube videos, taking Screenshots, Trimming videos of the Downloaded medias

# Operation
- Just send a telegram media to the bot chat and give /download command as replay to the media
- Follow the bot instructions

# Advantage
- Doesn't need any repeated uploads & downloads for different operations and even in YouTube downloads 😉
- Will get all you want in a single download. Save your time... be in your mood 🧐
- **Finally:** If you are a movie channel admin, the bot is all yours 🥳

## Easy Way :

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/m4mallu/intermedibot)

Note: YouTube downloads having some errors when deployed in heroku. Try other vps to test if possible.

## On linux Servers Or VPS

Create **config.py** with variables as given below

**An example `config.py` file could be:**

[Note: All the variables are mandatory]

```python3
class Development(Config):
  APP_ID = "55315485"
  API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
  TG_BOT_TOKEN = "624442654:nhs6sgvhh6776gfnhsbnTGFbb9277nNbb"
  AUTH_USERS = [245588455,246456588,3452256266]
  PRE_FILE_TXT = "@MovieKeralam."
```
**Pre requesties are : ffmpeg** :
``` sh
sudo apt-get install ffmpeg
```
After creating the config file, open a terminal in the bot directory and run the following commands (Don' run as root !)

```sh
virtualenv -p python3 venv
. ./venv/bin/activate
pip install -r requirements.txt
python bot.py
```
## [@BotFather](https://telegram.dog/BotFather) Commands

```
start - Check if the Bot is Online and for How to use this Bot
download - Download the media for further procesings (Give as a Replay to any telegram media)
```

## LICENSE
- GPLv3

## Credits :
[SpEcHiDe](https://github.com/SpEcHiDe) for his [AnyDLBot](https://github.com/SpEcHiDe/AnyDLBot)

[HASIBUL KOBIR](https://t.me/ABoyWhoLivesAlone) For his Valuable supports !

[DAN](https://t.me/haskell) for his [Pyrogram](https://github.com/pyrogram/pyrogram) Library