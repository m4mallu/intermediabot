# File Name     - YouTube
# Description   - YouTube link downloader function. This will extracts the input link.
# Owner         - Kiddilan
# Repo          - https://github.com/m4mallu
# Tg Uid        - @kiddilan
# Channel       - @MovieKeralam
# ---------------------------------------------------------------------------------- #

import logging
import os
import pyrogram
import time

from translation import Translation
from pyrogram import Client, Filters, InlineKeyboardMarkup, InlineKeyboardButton
from helper.ytdlfunc import extractYt, create_buttons

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

config_path = os.path.join(os.getcwd(), 'config.py')
if os.path.isfile(config_path):
    from config import Config
else:
    from sample_config import Config

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"


@Client.on_message(Filters.regex(ytregex))
async def ytdl(_, message):
    if message.from_user.id not in Config.AUTH_USERS:
        await _.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)
        a = await message.reply_text(text=Translation.NOT_AUTH_TXT)
        time.sleep(8)
        await a.delete()
        return
    saved_file_path = os.getcwd() + "/" + "downloads" + "/" + str(message.from_user.id) + "/"
    if not os.path.isdir(saved_file_path):
        os.makedirs(saved_file_path)
    dl_folder = [f for f in os.listdir(saved_file_path)]
    for f in dl_folder:
        try:
            os.remove(os.path.join(saved_file_path, f))
        except IndexError:
            pass
    url = message.text.strip()
    await message.reply_chat_action("typing")
    try:
        title, thumbnail_url, formats = extractYt(url)
    except Exception:
        await message.delete()
        await message.reply_text(
            text=Translation.FAILED_LINK,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Close", callback_data="close")]
                ])
        )
        return
    buttons = InlineKeyboardMarkup(list(create_buttons(formats)))
    sentm = await message.reply_text(text=Translation.PROCESS_START)
    try:
        # Todo add webp image support in thumbnail by default not supported by pyrogram
        # https://www.youtube.com/watch?v=lTTajzrSkCw
        await message.reply_photo(thumbnail_url, caption=title, reply_markup=buttons)
        await sentm.delete()
    except Exception as e:
        try:
            thumbnail_url = "https://telegra.ph/file/8d931a87ca1b644e03341.gif"
            await message.reply_photo(thumbnail_url, caption=title, reply_markup=buttons)
            await sentm.delete()
        except IndexError:
            pass
