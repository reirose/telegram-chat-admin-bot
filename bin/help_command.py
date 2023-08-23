from telegram import Update
from telegram.ext import ContextTypes

from bin.is_private import is_private


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mes = update.message

    if not is_private(update):
        return

    help_text = ("<b>Available commands\n</b>"
                 "All users:\n"
                 "<code>/report</code> — report a message to administrator\n"
                 "<code>/roll</code> — roll a number from 1 to 100\n\n"
                 "Moderators:\n"
                 "<code>/ban</code> — ban a user from chat (by reply)\n"
                 "<code>/kick</code> — kick a user from chat (by reply)\n"
                 "<code>/mute [n]</code> — mute a user for <code>n</code> minutes (by reply)\n\n"
                 "Administrators:\n"
                 "<code>/promote [type]</code> — promote a user. Available types: VIP, Moderator, "
                 "Administrator (case sensitive) (by reply)\n"
                 "<code>/vip_mode</code> — toggle VIP mode in a chat. VIP mode allows only VIPs, moderators and "
                 "administrators to write.\n")

    await mes.reply_text(text=help_text,
                         parse_mode="HTML")
