from telegram._chatmember import ChatMemberOwner


async def get_admins(update):
    return await update.message.chat.get_administrators()


def is_admin(user_id, admins):
    return user_id in [x.user.id for x in admins]


class RoleChecker:

    def __init__(self, update, role):
        self.update = update
        self.role = role

    async def check(self):
        admins = await get_admins(self.update)
        if not is_admin(self.update.message.from_user.id, admins):
            return False

        user = await self.update.message.chat.get_member(self.update.message.from_user.id)
        return user.custom_title == self.role or type(user) == ChatMemberOwner


class IsAdministrator(RoleChecker):

    def __init__(self, update):
        super().__init__(update, "Administrator")


class IsModerator(RoleChecker):

    def __init__(self, update):
        super().__init__(update, "Moderator")


class IsVIP(RoleChecker):

    def __init__(self, update):
        super().__init__(update, "VIP")


async def is_administrator(update):
    checker = IsAdministrator(update)
    return await checker.check()


async def is_moderator(update):
    checker = IsModerator(update)
    return await checker.check()


async def is_VIP(update):
    checker = IsVIP(update)
    return await checker.check()
