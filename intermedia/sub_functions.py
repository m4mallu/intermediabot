# File Name     - Sub Functions
# Description   - Sub functions like Set Thumbnail, View Thumbnail, Delete Thumbnail & Close Button Functions
# Owner         - Kiddilan
# Repo          - https://github.com/m4mallu
# Tg Uid        - @kiddilan
# Channel       - @MovieKeralam
# --------------------------------------------------------------------------------------------------------- #
import os
import os.path
import time
import pyrogram
import logging

from translation import Translation
from intermedia.help_text import bot_settings

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

config_path = os.path.join(os.getcwd(), 'config.py')
if os.path.isfile(config_path):
    from config import Config
else:
    from sample_config import Config

@pyrogram.Client.on_message(pyrogram.Filters.photo)
async def save_photo(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await update.delete()
        a = await update.reply_text(text=Translation.NOT_AUTH_TXT)
        time.sleep(5)
        await a.delete()
        await bot_settings(bot, update)
        return
    try:
        await bot.delete_messages(chat_id=update.chat.id, message_ids=update.message_id)
        thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
        await bot.download_media(message=update, file_name=thumb_image_path)
        await update.delete()
        a1 = await update.reply_text(text=Translation.SAVED_CUSTOM_THUMB_NAIL)
        time.sleep(6)
        await a1.delete()
    except IndexError:
        pass

async def view_thumbnail(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        b = await update.message.reply_text(text=Translation.NOT_AUTH_TXT)
        time.sleep(8)
        await b.delete()
        await bot_settings(bot, update)
        return
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
    if os.path.exists(thumb_image_path):
        await bot.send_photo(
            chat_id=update.message.chat.id,
            photo=thumb_image_path,
            caption=Translation.THUMB_CAPTION,
            reply_to_message_id=update.message.message_id,
            reply_markup=pyrogram.InlineKeyboardMarkup(
                [[pyrogram.InlineKeyboardButton("DEL THUMB", callback_data="conf_thumb"),
                 pyrogram.InlineKeyboardButton("Back", callback_data="settings")]]))

    else:
        await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
        c = await bot.send_message(chat_id=update.message.chat.id, text=Translation.NO_THUMB)
        time.sleep(5)
        await c.delete()
        await bot_settings(bot, update)


async def delete_thumbnail(bot, update):
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
    try:
        os.remove(thumb_image_path)
        a = await bot.send_message(chat_id=update.message.chat.id, text=Translation.DEL_CUSTOM_THUMB_NAIL)
        time.sleep(5)
        await a.delete()
        await bot_settings(bot, update)
    except IndexError:
        pass


async def del_thumb_confirm(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        b = await update.message.reply_text(text=Translation.NOT_AUTH_TXT)
        time.sleep(8)
        await b.delete()
        await bot_settings(bot, update)
        return
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
    if os.path.exists(thumb_image_path):
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=Translation.DEL_THUMB_CONFIRM,
            reply_to_message_id=update.message.message_id,
            reply_markup=pyrogram.InlineKeyboardMarkup(
                [[pyrogram.InlineKeyboardButton("✅ Sure, Delete It", callback_data="del_thumb"),
                 pyrogram.InlineKeyboardButton("Back", callback_data="settings")]]))
    else:
        await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
        b1 = await bot.send_message(chat_id=update.message.chat.id, text=Translation.NO_THUMB)
        time.sleep(5)
        await b1.delete()
        await bot_settings(bot, update)


async def close_button(bot, update):
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)