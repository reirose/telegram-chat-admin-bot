from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from random import randint


async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mes = update.message

    reply_text = f"<b>{mes.from_user.first_name}</b> rolled <code>{randint(0, 100)}</code>"
    await mes.reply_text(text=reply_text,
                         reply_to_message_id=mes.message_id,
                         parse_mode="HTML")


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mes = update.message

    n = 0
    chat_name = mes.chat.title

    for admin_id in [x.user.id for x in await mes.chat.get_administrators()]:
        try:
            await context.bot.send_message(chat_id=admin_id,
                                           text=f"Got an alert from <b>{chat_name}</b> chat",
                                           parse_mode="HTML")
            n += 1
        except TelegramError:
            pass

    reply_text = f"<b>Report sent to {n} admins!</b>"
    await mes.reply_text(text=reply_text,
                         parse_mode="HTML",
                         reply_to_message_id=mes.message_id)
