import os

class Config(object):    
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
    # The Telegram API things
    APP_ID = os.environ.get("APP_ID")
    API_HASH = os.environ.get("API_HASH")
    # Get these values from my.telegram.org
    # Array to store users who are authorized to use the bot
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
    # Telegram maximum file upload size
    MAX_FILE_SIZE = 50000000
    TG_MAX_FILE_SIZE = 1572864000
    MAX_MESSAGE_LENGTH = 4096
    PRE_FILE_TXT = os.environ.get("PRE_FILE_TXT", "@MovieKeralam.")
