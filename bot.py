# File Name     - Bot
# Description   - Main Function
# Owner         - Kiddilan
# Repo          - https://github.com/m4mallu
# Tg Uid        - @kiddilan
# Channel       - @MovieKeralam
# ----------------------------------------- #

import os
import pyrogram
if bool(os.environ.get("env", False)):
    from sample_config import Config
else:
    from config import Config

if __name__ == "__main__" :
    intermedia = dict(root="intermedia")
    app = pyrogram.Client(
        "intermediabot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=intermedia
    )
    app.run()
