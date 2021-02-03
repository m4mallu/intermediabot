# File Name     - help
# Description   - Start & Help functions for intermedia bot
# Owner         - Kiddilan
# Repo          - https://github.com/m4mallu
# Tg Uid        - @kiddilan
# Channel       - @MovieKeralam
# ---------------------------------------------------------------------------------------- #

import pyrogram
from translation import Translation


@pyrogram.Client.on_message(pyrogram.Filters.command(["start"]), group=0)
async def start(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.first_name),
        disable_web_page_preview=True,
        reply_markup=pyrogram.InlineKeyboardMarkup(
            [
                [pyrogram.InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
            ])
    )
    await update.delete()
    raise pyrogram.StopPropagation()


async def bot_settings(bot, update):
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
    await bot.send_message(
        chat_id=update.message.chat.id,
        text=Translation.SETTINGS_TEXT,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message.message_id,
        reply_markup=pyrogram.InlineKeyboardMarkup(
            [
                [pyrogram.InlineKeyboardButton("View Thumb", callback_data="view_thumb"),
                 pyrogram.InlineKeyboardButton("Del Thumb", callback_data="conf_thumb")],
                [pyrogram.InlineKeyboardButton("Help", callback_data="start_help"),
                 pyrogram.InlineKeyboardButton("Close", callback_data="close")]
            ])
    )


async def start_bot(bot, update):
    await bot.delete_messages(chat_id=update.message.chat.id, message_ids=update.message.message_id)
    await bot.send_message(
        chat_id=update.message.chat.id,
        text=Translation.START_TEXT.format(update.from_user.first_name),
        disable_web_page_preview=True,
        reply_markup=pyrogram.InlineKeyboardMarkup(
            [
                [pyrogram.InlineKeyboardButton("⚙️ Settings", callback_data="bot_settings")]
            ])
    )
