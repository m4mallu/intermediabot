# File Name     - Generate Screenshot
# Description   - Generating Screenshots for file formatting & YouTube DL functions
# Owner         - MalluBoy
# Repo          - https://github.com/m4mallu
# Tg Id         - @space4renjith
# Channel       - @MovieKeralam
# -------------------------------------------------------------------------------- #

import os
import shutil
from pyrogram import InputMediaPhoto
from helper.gen_ss_help import generate_screen_shots
from translation import Translation
from intermedia.trim_video import trim


async def generate_screen_shot(bot, update):
    tmp_directory_for_each_user = os.path.join(os.getcwd(), "Screenshots", str(update.from_user.id))
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    ss_folder = [f for f in os.listdir(tmp_directory_for_each_user)]
    for f in ss_folder:
        try:
            os.remove(os.path.join(tmp_directory_for_each_user, f))
        except IndexError:
            pass
    saved_file_path = os.getcwd() + "/" + "downloads" + "/" + str(update.from_user.id) + "/"
    for file in os.listdir(saved_file_path):
        dir_content = (os.path.join(saved_file_path, file))
        if dir_content is not None:
            images = await generate_screen_shots(
                dir_content,
                tmp_directory_for_each_user,
                5,
                9
            )
            media_album_p = []
            if images is not None:
                i = 0
                for image in images:
                    if os.path.exists(image):
                        if i == 0:
                            media_album_p.append(
                                InputMediaPhoto(
                                    media=image,
                                    caption=Translation.CAPTION_TEXT,
                                    parse_mode="html"
                                )
                            )
                        else:
                            media_album_p.append(
                                InputMediaPhoto(
                                    media=image
                                )
                            )
                        i = i + 1
            await bot.send_chat_action(chat_id=update.message.chat.id, action="upload_photo")
            await bot.send_media_group(
                chat_id=update.message.chat.id,
                disable_notification=True,
                reply_to_message_id=update.message.message_id,
                media=media_album_p
            )
            try:
                shutil.rmtree(tmp_directory_for_each_user)
                await trim(bot, update)
            except IndexError:
                pass
