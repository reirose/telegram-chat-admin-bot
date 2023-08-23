import logging
import sys

from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Import bot command functions
from bin.start import start
from bin.help_command import help_command
from bin.users_commands import roll, report
from bin.parameters_parser import parameters_parser
from bin.administrator_commands import restrict_user, mute, promote_user, vip_mode, message_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main() -> None:

    # Parse command line parameters
    params = parameters_parser(sys.argv)
    app = Application.builder().token(params.get("TOKEN")).build()

    # Add handlers for bot commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler(["roll", 'r'], roll))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler(["kick", 'ban'], restrict_user))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("promote", promote_user))
    app.add_handler(CommandHandler("vip_mode", vip_mode))

    # Handle all other messages for VIP mode
    app.add_handler(MessageHandler(filters=filters.ALL, callback=message_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
