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

if bool(os.environ.get("env", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation


@pyrogram.Client.on_message(pyrogram.Filters.photo)
async def save_photo(bot, update):
    # receive single photo
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.delete_messages(chat_id=update.chat.id, message_ids=update.message_id)
        a = await update.reply_text(text=Translation.NOT_AUTH_TXT)
        time.sleep(8)
        await a.delete()
        return
    await bot.delete_messages(chat_id=update.chat.id, message_ids=update.message_id)
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
    await bot.download_media(message=update, file_name=thumb_image_path)
    await update.delete()
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.SAVED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id,
        reply_markup=pyrogram.InlineKeyboardMarkup(
            [
                [pyrogram.InlineKeyboardButton("Close", callback_data="close")]
            ])
    )


async def view_thumbnail(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
        b = await update.message.reply_text(text=Translation.NOT_AUTH_TXT)
        time.sleep(8)
        await b.delete()
        return
    await bot.delete_messages(
        chat_id=update.message.chat.id,
        message_ids=update.message.message_id
    )
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
    if os.path.exists(thumb_image_path):
        await bot.send_photo(
            chat_id=update.message.chat.id,
            photo=thumb_image_path,
            caption=Translation.THUMB_CAPTION,
            reply_to_message_id=update.message.message_id,
            reply_markup=pyrogram.InlineKeyboardMarkup(
                [
                    [pyrogram.InlineKeyboardButton("DEL THUMB", callback_data="conf_thumb"),
                     pyrogram.InlineKeyboardButton("Back", callback_data="settings")]
                ])
        )

    else:
        await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=Translation.NO_THUMB,
            reply_to_message_id=update.message.message_id,
            reply_markup=pyrogram.InlineKeyboardMarkup(
                [
                    [pyrogram.InlineKeyboardButton("Back", callback_data="settings")]
                ])
        )


async def delete_thumbnail(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
        c = await update.message.reply_text(text=Translation.NOT_AUTH_TXT)
        time.sleep(8)
        await c.delete()
        return
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/"
    media_files = os.listdir(thumb_image_path)
    if len(media_files) == 0:
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=Translation.NO_THUMB,
            reply_to_message_id=update.message.message_id,
            reply_markup=pyrogram.InlineKeyboardMarkup(
                [
                    [pyrogram.InlineKeyboardButton("Back", callback_data="settings")]
                ])
        )
    else:
        thumb_folder = [f for f in os.listdir(thumb_image_path)]
        for f in thumb_folder:
            try:
                os.remove(os.path.join(thumb_image_path, f))
            except IndexError:
                pass
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=Translation.DEL_CUSTOM_THUMB_NAIL,
            reply_to_message_id=update.message.message_id,
            reply_markup=pyrogram.InlineKeyboardMarkup(
                [
                    [pyrogram.InlineKeyboardButton("Back", callback_data="settings")]

                ])
        )


async def close_button(bot, update):
    await bot.delete_messages(
        chat_id=update.message.chat.id,
        message_ids=update.message.message_id
    )


async def del_thumb_confirm(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
        d = await update.message.reply_text(text=Translation.NOT_AUTH_TXT)
        time.sleep(8)
        await d.delete()
        return
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
    await bot.send_message(
        chat_id=update.message.chat.id,
        text=Translation.DEL_THUMB_CONFIRM,
        reply_to_message_id=update.message.message_id,
        reply_markup=pyrogram.InlineKeyboardMarkup(
            [
                [pyrogram.InlineKeyboardButton("✅ Sure", callback_data="del_thumb"),
                 pyrogram.InlineKeyboardButton("Back", callback_data="settings")]

            ])
    )