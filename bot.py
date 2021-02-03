# File Name     - Bot
# Description   - Main Function
# Owner         - Kiddilan
# Repo          - https://github.com/m4mallu
# Tg Uid        - @kiddilan
# Channel       - @MovieKeralam
# ----------------------------------------- #
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import pyrogram

logging.getLogger("pyrogram").setLevel(logging.WARNING)

if bool(os.environ.get("env", False)):
    from sample_config import Config
else:
    from config import Config

if __name__ == "__main__":
    intermedia = dict(root="intermedia")
    app = pyrogram.Client(
        "intermediabot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=intermedia
    )
    app.run()
