from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mes = update.message

    greeting_text = ("<b>Hello!</b>\n"
                     "This bot is used to help administrators of big chats.\n"
                     "To see more info, please press /help (works only in PM)")

    await mes.reply_text(text=greeting_text,
                         parse_mode="HTML")
