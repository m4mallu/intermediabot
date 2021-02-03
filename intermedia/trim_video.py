# File Name     - Trim Video
# Description   - Sample video making function from the downloaded media.
# Owner         - Kiddilan
# Repo          - https://github.com/m4mallu
# Tg Uid        - @kiddilan
# Channel       - @MovieKeralam
# ---------------------------------------------------------------------- #
import time
import os
import pyrogram

from helper.gen_ss_help import cult_small_video
from translation import Translation


async def trim(bot, update):
    output_directory = os.path.join(os.getcwd(), "sample_video")
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)
    trim_folder = [f for f in os.listdir(output_directory)]
    for f in trim_folder:
        try:
            os.remove(os.path.join(output_directory, f))
        except IndexError:
            pass
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(update.from_user.id) + ".jpg"
    if not os.path.exists(thumb_image_path):
        thumb_image_path = None
    saved_file_path = os.getcwd() + "/" + "downloads" + "/" + str(update.from_user.id) + "/"
    for file in os.listdir(saved_file_path):
        dir_content = (os.path.join(saved_file_path, file))
        if dir_content is not None:
            start_time = "00:04:00"
            end_time = "00:05:00"
            o = await cult_small_video(dir_content, output_directory, start_time, end_time)
            # Give a code pause for 30Sec to trim the video
            time.sleep(30)
            await bot.send_chat_action(chat_id=update.message.chat.id, action="upload_video")
            if o is not None:
                await bot.send_video(
                    chat_id=update.message.chat.id,
                    video=o,
                    thumb=thumb_image_path,
                    caption="Sample Video:",
                    supports_streaming=True,
                    reply_to_message_id=update.message.message_id
                )
            try:
                os.remove(o)
                await bot.send_message(
                    text=Translation.MAKE_A_COPY_TEXT,
                    chat_id=update.message.chat.id,
                    reply_to_message_id=update.message.message_id,
                    reply_markup=pyrogram.InlineKeyboardMarkup(
                        [
                            [pyrogram.InlineKeyboardButton("📘 Document", callback_data="d_copy"),
                             pyrogram.InlineKeyboardButton("🎞 Video", callback_data="v_copy")],
                            [pyrogram.InlineKeyboardButton(" Close", callback_data="clear_med")]
                        ])
                )
            except IndexError:
                pass
