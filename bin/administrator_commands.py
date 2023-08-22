from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from time import sleep, time

from bin.is_administrator import is_administrator, is_moderator
from bin.is_private import is_private


async def kick_or_ban(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    print(context.args)
    mes = update.message
    if ((not await is_moderator(update)
         and not await is_administrator(update))  # I wanna kms for this indentation but I won't redo this
            or is_private(update)
            or not mes.reply_to_message):
        return

    try:
        await context.bot.banChatMember(chat_id=mes.chat_id,
                                        user_id=mes.reply_to_message.from_user.id)

        if "/kick" in mes.text:
            sleep(1)
            await context.bot.unbanChatMember(chat_id=mes.chat_id,
                                              user_id=mes.reply_to_message.from_user.id)
    except BadRequest as e:
        await mes.reply_text(text=f'Bad request: {e}',
                             reply_to_message_id=mes.message_id)


async def mute(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    mes = update.message

    if ((not await is_moderator(update)
         and not await is_administrator(update))
            or is_private(update)
            or not mes.reply_to_message
            or not context.args):
        return

    try:
        time_until = int(context.args[0]) * 60
    except (IndexError, ValueError) as e:
        await mes.reply_text(text=f'Error: {e}',
                             reply_to_message_id=mes.message_id)
        return
    try:
        perm = ChatPermissions()
        perm.no_permissions()
        await context.bot.restrictChatMember(chat_id=mes.chat_id,
                                             user_id=mes.reply_to_message.from_user.id,
                                             until_date=time()+time_until,
                                             permissions=perm)
    except BadRequest as e:
        await mes.reply_text(text=f'Bad request: {e}',
                             reply_to_message_id=mes.message_id)
        return

    await mes.reply_text(text=f"<b>{mes.reply_to_message.from_user.first_name}</b> had been muted"
                              f" for <code>{int((time_until / 60) // 60)}h {int((time_until / 60) % 60)}m</code>",
                         parse_mode="HTML")
