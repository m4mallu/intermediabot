# File Name     - Multimedia
# Description   - Tg file downloading, Renaming and converting to Doc / Video
# Owner         - Kiddilan
# Repo          - https://github.com/m4mallu
# Tg Uid        - @kiddilan
# Channel       - @MovieKeralam
# ----------------------------------------------------------------------------- #

import os
import time
import pyrogram
import logging

from translation import Translation
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.display_progress import progress_for_pyrogram
from intermedia.generate_screenshot import generate_screen_shot
from intermedia.help_text import bot_settings
from bot import cache1, cache2

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


# -------------------------------- Bot will download media and rename as required -------------------------------------#

@pyrogram.Client.on_message(pyrogram.Filters.command(["download"]), group=1)
async def download_media(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.delete_messages(chat_id=update.chat.id, message_ids=update.message_id)
        a0 = await update.reply_text(text=Translation.NOT_AUTH_TXT)
        time.sleep(8)
        await a0.delete()
        await bot_settings(bot, update)
        raise pyrogram.StopPropagation()
    else:
        if ("download" in update.text) and (update.reply_to_message is not None):
            await update.delete()
            download_location = os.path.join(os.getcwd(), "downloads", str(update.chat.id))
            if not os.path.isdir(download_location):
                os.makedirs(download_location)
            dl_folder = [f for f in os.listdir(download_location)]
            for f in dl_folder:
                try:
                    os.remove(os.path.join(download_location, f))
                except IndexError:
                    pass
            saved_file_path = download_location + "/" + "media_file.mkv"
            a = await bot.send_message(
                chat_id=update.chat.id,
                text=Translation.DOWNLOAD_START,
                reply_to_message_id=update.message_id
            )
            c_time = time.time()
            await bot.download_media(
                message=update.reply_to_message,
                file_name=saved_file_path,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.DOWNLOAD_START,
                    a,
                    c_time
                )
            )
            if saved_file_path is not None:
                try:
                    await bot.delete_messages(chat_id=update.chat.id, message_ids=a.message_id)
                    b = await bot.send_message(
                        text=Translation.SAVED_RECVD_DOC_FILE,
                        chat_id=update.chat.id,
                        reply_to_message_id=update.message_id,
                        reply_markup=pyrogram.ForceReply()
                    )
                    cache1[id] = b.message_id
                    raise pyrogram.StopPropagation()
                except IndexError:
                    pass


#################### After downloading the file user need to confirm the process want to execute #######################
@pyrogram.Client.on_message(pyrogram.Filters.text, group=2)
async def select_option(bot, update):
    file_name = update.text
    extensions = Translation.EXTENSIONS
    saved_file_path = os.getcwd() + "/" + "downloads" + "/" + str(update.from_user.id) + "/"
    if not os.path.isdir(saved_file_path):
        os.makedirs(saved_file_path)
    if len(os.listdir(saved_file_path)) == 1:
        if file_name.endswith(tuple(extensions)):
            if update.reply_to_message is not None:
                await bot.delete_messages(chat_id=update.chat.id, message_ids=cache1[id])
                saved_file_path = os.getcwd() + "/" + "downloads" + "/" + str(
                    update.from_user.id) + "/" + "media_file.mkv"
                new_file_name = saved_file_path.replace('media_file.mkv', '') + file_name
                os.rename(saved_file_path, new_file_name)
                await update.delete()
                try:
                    c = await bot.send_message(
                        text=Translation.FILE_TYPE_SELEC.format(file_name),
                        chat_id=update.chat.id,
                        reply_to_message_id=update.message_id,
                        reply_markup=pyrogram.InlineKeyboardMarkup(
                            [
                                [pyrogram.InlineKeyboardButton(text="📚Document", callback_data="rename_doc"),
                                 pyrogram.InlineKeyboardButton("🎞Video", callback_data="convert_video")]
                            ])
                    )
                    cache2[id] = c.message_id
                except IndexError:
                    pass
        else:
            await update.delete()
            x1 = await bot.send_message(
                text=Translation.INPUT_ERROR,
                chat_id=update.chat.id,
                reply_to_message_id=update.message_id
            )
            time.sleep(8)
            await x1.delete()
    else:
        if "https://youtu" not in update.text:
            await update.delete()
            x2 = await bot.send_message(
                text=Translation.NO_SPAM_MSG,
                chat_id=update.chat.id,
                reply_to_message_id=update.message_id
            )
            time.sleep(5)
            await x2.delete()


############################################## Upload the file as Document #############################################
async def rename_file(bot, update):
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=cache2[id])
    saved_file_path = os.getcwd() + "/" + "downloads" + "/" + str(update.from_user.id) + "/"
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
    if not os.path.exists(thumb_image_path):
        thumb_image_path = None
    description = Translation.CUSTOM_CAPTION_DOC
    extensions = Translation.EXTENSIONS
    for file in os.listdir(saved_file_path):
        if file.endswith(tuple(extensions)):
            dir_content = (os.path.join(saved_file_path, file))
            if dir_content is not None:
                d = await bot.send_message(
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
                        d,
                        c_time
                    )
                )
                try:
                    await d.delete()
                    e = await bot.send_message(text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG, chat_id=update.message.chat.id)
                    time.sleep(5)
                    await e.delete()
                    await generate_screen_shot(bot, update)
                except IndexError:
                    pass


############################################## Upload the file as Video ################################################
async def convert_to_video(bot, update):
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=cache2[id])
    saved_file_path = os.getcwd() + "/" + "downloads" + "/" + str(update.from_user.id) + "/"
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
    if not os.path.exists(thumb_image_path):
        thumb_image_path = None
    description = Translation.CUSTOM_CAPTION_VIDEO
    extensions = Translation.EXTENSIONS
    for file in os.listdir(saved_file_path):
        if file.endswith(tuple(extensions)):
            dir_content = (os.path.join(saved_file_path, file))
            if dir_content is not None:
                metadata = extractMetadata(createParser(dir_content))
                if metadata.has("duration"):
                    duration = metadata.get('duration').seconds
                    f = await bot.send_message(
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
                            f,
                            c_time
                        )
                    )
                    try:
                        await f.delete()
                        g = await bot.send_message(text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG, chat_id=update.message.chat.id)
                        time.sleep(5)
                        await g.delete()
                        await generate_screen_shot(bot, update)
                    except IndexError:
                        pass
