"""
Runner for the C.A.B.A.L. Telegram Bot.
"""
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from ResourceManager.resource_manager import ResourceManager
from StringConstants.string_constants import EnglishStrings
from Utils import file_reader


def main():
    """
    Main runner function for the C.A.B.A.L. Bot.
    """
    resource_handler = ResourceManager(file_reader.read_token('resources/token.conf'))

    updater = Updater(resource_handler.token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("echo", echo))
    dispatcher.add_handler(MessageHandler(Filters.command, unkown_command))

    updater.start_polling()
    updater.idle()


def echo(bot, updater):
    """
    Command returns the send message back to the sending chat.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text=updater.message.text)



def unkown_command(bot, updater):
    """
    Handles unkown commands send to the bot.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text=EnglishStrings.UNKOWN_COMMAND)


if __name__ == "__main__":
    main()
