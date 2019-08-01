"""
Runner for the C.A.B.A.L. Telegram Bot.
"""
from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from ResourceManager.resource_manager import ResourceManager
from StringConstants.string_constants import EnglishStrings
from Utils import file_reader, helper

RESOURCE_HANDLER = ResourceManager(file_reader.read_token('resources/token.conf'))
HELPER = None



def main():
    """
    Main runner function for the C.A.B.A.L. Bot.
    """
    global HELPER
    global RESOURCE_HANDLER

    updater = Updater(RESOURCE_HANDLER.token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_me))
    dispatcher.add_handler(CommandHandler("echo", echo))
    dispatcher.add_handler(CommandHandler("id", chat_id))
    dispatcher.add_handler(MessageHandler(Filters.command, unkown_command))

    HELPER = helper.Helper(dispatcher)

    updater.start_polling()
    updater.idle()


def echo(bot, updater):
    """
    Usage: /echo text
    Result: This will print a message containing "text"
    """
    input_text = updater.message.text
    output_text = input_text.replace("/echo ", '')
    bot.send_message(chat_id=updater.message.chat_id,
                     text=output_text)

def chat_id(bot, updater):
    """
    Result: Prints the current chat id.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text=updater.message.chat_id)


def help_me(bot, updater):
    """
    Prints the help message.
    """
    global HELPER
    bot.send_message(chat_id=updater.message.chat_id,
                     text=HELPER.help_string,
                     parse_mode=ParseMode.MARKDOWN)


def unkown_command(bot, updater):
    """
    Handles unkown commands send to the bot.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text=EnglishStrings.UNKOWN_COMMAND)


if __name__ == "__main__":
    main()
