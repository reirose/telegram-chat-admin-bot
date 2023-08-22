from telegram import Update


def is_private(update: Update) -> bool:
    if update.message.chat.id < 0:
        return False

    return True
