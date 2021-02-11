# File Name     - Make Another Copy
# Description   - Make another copy of a converted file. If a file is converted and send to the chat id, can have the
#                 option to send it as a video also. This will be very useful for movie channel owners to convert
#                 a Tg / YouTube dl media in to Video & Doc file in a single download.
# Owner         - MalluBoy
# Repo          - https://github.com/m4mallu
# Tg Id         - @space4renjith
# Channel       - @MovieKeralam
# ------------------------------------------------------------------------------------------------------------------- #

import os
import time
import shutil
import pyrogram

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from translation import Translation
from helper.display_progress import progress_for_pyrogram


async def convert_to_doc_copy(bot, update):
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
    saved_file_path = os.getcwd() + "/" + "downloads" + "/" + str(update.from_user.id) + "/"
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
    description = Translation.CUSTOM_CAPTION_DOC
    if not os.path.exists(thumb_image_path):
        thumb_image_path = None
    for file in os.listdir(saved_file_path):
        dir_content = (os.path.join(saved_file_path, file))
        if dir_content is not None:
            a = await bot.send_message(
                chat_id=update.message.chat.id,
                text=Translation.UPLOAD_START,
                reply_to_message_id=update.message.message_id
            )
            c_time = time.time()
            await bot.send_document(
                chat_id=update.message.chat.id,
                document=dir_content,
                thumb=thumb_image_path,
                caption=description,
                reply_to_message_id=update.message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    a,
                    c_time
                )
            )
            try:
                shutil.rmtree(saved_file_path)
                await a.delete()
                await bot.send_message(
                    text=Translation.THANKS_MESSAGE,
                    chat_id=update.message.chat.id,
                    reply_to_message_id=update.message.message_id,
                    reply_markup=pyrogram.InlineKeyboardMarkup(
                        [
                            [pyrogram.InlineKeyboardButton("View Thumb", callback_data="view_thumb"),
                             pyrogram.InlineKeyboardButton("Del Thumb", callback_data="conf_thumb")],
                            [pyrogram.InlineKeyboardButton("Help", callback_data="start_help"),
                             pyrogram.InlineKeyboardButton("Close", callback_data="close")]
                        ])
                )
            except IndexError:
                pass


async def convert_to_video_copy(bot, update):
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
    saved_file_path = os.getcwd() + "/" + "downloads" + "/" + str(update.from_user.id) + "/"
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
    description = Translation.CUSTOM_CAPTION_VIDEO
    if not os.path.exists(thumb_image_path):
        thumb_image_path = None
    for file in os.listdir(saved_file_path):
        dir_content = (os.path.join(saved_file_path, file))
        if dir_content is not None:
            metadata = extractMetadata(createParser(dir_content))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
                b = await bot.send_message(
                    chat_id=update.message.chat.id,
                    text=Translation.UPLOAD_START,
                    reply_to_message_id=update.message.message_id
                )
                c_time = time.time()
                await bot.send_video(
                    chat_id=update.message.chat.id,
                    video=dir_content,
                    duration=duration,
                    caption=description,
                    thumb=thumb_image_path,
                    supports_streaming=True,
                    reply_to_message_id=update.message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        b,
                        c_time
                    )
                )
                try:
                    shutil.rmtree(saved_file_path)
                    await b.delete()
                    await bot.send_message(
                        text=Translation.THANKS_MESSAGE,
                        chat_id=update.message.chat.id,
                        reply_to_message_id=update.message.message_id,
                        reply_markup=pyrogram.InlineKeyboardMarkup(
                            [
                                [pyrogram.InlineKeyboardButton("View Thumb", callback_data="view_thumb"),
                                 pyrogram.InlineKeyboardButton("Del Thumb", callback_data="conf_thumb")],
                                [pyrogram.InlineKeyboardButton("Help", callback_data="start_help"),
                                 pyrogram.InlineKeyboardButton("Close", callback_data="close")]
                            ])
                    )
                except IndexError:
                    pass


async def clear_media(bot, update):
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
    saved_file_path = os.getcwd() + "/" + "downloads" + "/" + str(update.from_user.id) + "/"
    shutil.rmtree(saved_file_path)
    await bot.send_message(
        text=Translation.THANKS_MESSAGE,
        chat_id=update.message.chat.id,
        reply_to_message_id=update.message.message_id,
        reply_markup=pyrogram.InlineKeyboardMarkup(
            [
                [pyrogram.InlineKeyboardButton("View Thumb", callback_data="view_thumb"),
                 pyrogram.InlineKeyboardButton("Del Thumb", callback_data="conf_thumb")],
                [pyrogram.InlineKeyboardButton("Help", callback_data="start_help"),
                 pyrogram.InlineKeyboardButton("Close", callback_data="close")]
            ])
    )
