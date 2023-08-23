from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from time import sleep, time
from typing import AnyStr

from bin.is_administrator import is_administrator, is_moderator, is_VIP
from bin.is_private import is_private

VIP_mode: bool = False


async def check_permission(update: Update, type_of: AnyStr, reply_needed: bool) -> bool:
    """
    Checking for some permissions to use the command
    :param update: Telegram Update object
    :param type_of: type of needed user level (admin, moderator or VIP)
    :param reply_needed: check if reply is needed
    :return: False if everything is okay, otherwise True  # Yes, this is inverted but why not
    """
    return (is_private(update) or
            (((not await is_moderator(update) if type_of in ["VIP", "Moderator"] else True)
              and not await is_administrator(update)
              and (not await is_VIP(update) if type_of in ["VIP", "Moderator"] else True))
             or not (update.message.reply_to_message if reply_needed else True)))


async def restrict_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Ban or kick user depending on the command passed
    """
    mes = update.message
    # check the >= Moderator level
    if await check_permission(update, "Moderator", True):
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


async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Mute user for n minutes
    """
    mes = update.message

    if await check_permission(update, "Moderator", True):
        return

    try:
        time_until = int(context.args[0]) * 60
    except (IndexError, ValueError):
        await mes.reply_text(text=f'Syntax error',
                             reply_to_message_id=mes.message_id)
        return
    try:
        perm = ChatPermissions()
        perm.no_permissions()
        await context.bot.restrictChatMember(chat_id=mes.chat_id,
                                             user_id=mes.reply_to_message.from_user.id,
                                             until_date=time() + time_until,
                                             permissions=perm)
    except BadRequest as e:
        await mes.reply_text(text=f'Bad request: {e}',
                             reply_to_message_id=mes.message_id)
        return

    await mes.reply_text(text=f"<b>{mes.reply_to_message.from_user.first_name}</b> had been muted"
                              f" for {int((time_until / 60) // 60)}h {int((time_until / 60) % 60)}m",
                         parse_mode="HTML")


async def vip_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Toggle VIP mode
    """
    mes = update.message

    if await check_permission(update, "Moderator", False):
        return

    global VIP_mode
    VIP_mode = not VIP_mode

    await mes.reply_text(text=f"<b>VIP mode {'activated' if VIP_mode else 'deactivated'}</b>.",
                         parse_mode="HTML")


async def promote_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Promote user to a certain level
    If "Administrator" is passed, allows him to do everything
    If "Moderator" is passed, allows him to mute, kick, ban users, delete or pin messages and manage calls
    If "VIP" is passed, allows him to invite users and avoid slow-mode
    """
    mes = update.message

    if await check_permission(update, "Administrator", False):
        return

    if not context.args:
        await mes.reply_text(text="Syntax error",
                             reply_to_message_id=mes.message_id)
        return

    try:
        user_id = mes.reply_to_message.from_user.id
        type_of = context.args[0]  # /promote Moderator
        #                            this is  ^^^^^^^^^ this argument
        await context.bot.promoteChatMember(chat_id=mes.chat_id,
                                            user_id=user_id,
                                            can_invite_users=True,
                                            can_promote_members=type_of == "Administrator",
                                            can_change_info=type_of == "Administrator",
                                            can_manage_chat=True,
                                            can_pin_messages=type_of in ["Administrator", "Moderator"],
                                            can_delete_messages=type_of in ["Administrator", "Moderator"],
                                            can_edit_messages=type_of in ["Administrator", "Moderator"],
                                            can_manage_topics=type_of == "Administrator",
                                            can_post_messages=type_of == "Administrator",
                                            can_restrict_members=type_of in ["Administrator", "Moderator"],
                                            can_manage_video_chats=type_of in ["Administrator", "Moderator"])

        # sets user role according to his privileges
        await context.bot.setChatAdministratorCustomTitle(chat_id=mes.chat_id,
                                                          user_id=user_id,
                                                          custom_title=type_of)
    except (BadRequest, IndexError) as e:
        print(e)
        return


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    handles all the messages during VIP mode
    """
    mes = update.message
    bot = context.bot

    if not VIP_mode:
        return

    if await check_permission(update, "VIP", False):
        await bot.deleteMessage(chat_id=mes.chat_id,
                                message_id=mes.message_id)
