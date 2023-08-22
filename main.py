import logging
import sys

from telegram.ext import Application, CommandHandler

from bin.start import start
from bin.users_commands import roll, report
from bin.help_command import help_command
from bin.parameters_parser import parameters_parser
from bin.administrator_commands import kick_or_ban, mute

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main() -> None:
    params = parameters_parser(sys.argv)
    app = Application.builder().token(params.get("TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler(["roll", 'r'], roll))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler(["kick", 'ban'], kick_or_ban))
    app.add_handler(CommandHandler("mute", mute))

    app.run_polling()


if __name__ == "__main__":
    main()
