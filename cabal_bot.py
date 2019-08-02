"""
Runner for the C.A.B.A.L. Telegram Bot.
"""
from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from Commands import ComTime, ComXkcd
from ResourceManager.resource_manager import ResourceManager
from StringConstants.string_constants import EnglishStrings
from Utils import access_control, file_reader, helper

RESOURCE_HANDLER = ResourceManager(file_reader.read_token('resources/token.conf'),
                                   file_reader.read_admin_id('resources/admin.conf'))
EXPANDED_FUNCTION_ACCESS = access_control.AccessControlFilter('resources/white.list')
NORMAL_HELPER = None
EXPANDED_HELPER = None
ADMIN_HELPER = None



def main():
    """
    Main runner function for the C.A.B.A.L. Bot.
    """
    global NORMAL_HELPER
    global EXPANDED_HELPER
    global ADMIN_HELPER
    global RESOURCE_HANDLER

    admin_only = access_control.AccessControlFilter('resources/admin.list')
    admin_only.add_chat_id(RESOURCE_HANDLER.admin_id)

    updater = Updater(RESOURCE_HANDLER.token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_me))
    dispatcher.add_handler(CommandHandler("echo", echo, pass_args=True))
    dispatcher.add_handler(CommandHandler("id", chat_id))
    dispatcher.add_handler(CommandHandler("time",
                                          time,
                                          filters=EXPANDED_FUNCTION_ACCESS))
    dispatcher.add_handler(CommandHandler("xkcd", xkcd, pass_args=True))

    dispatcher.add_handler(CommandHandler("vip", vip), group=1)

    dispatcher.add_handler(CommandHandler("addChat",
                                          add_chat,
                                          pass_args=True,
                                          filters=admin_only),
                           group=666)
    dispatcher.add_handler(MessageHandler(Filters.command, unkown_command))

    NORMAL_HELPER = helper.Helper(dispatcher)
    EXPANDED_HELPER = helper.Helper(dispatcher, [0, 1])
    ADMIN_HELPER = helper.Helper(dispatcher, [0, 1, 666])

    updater.start_polling()
    updater.idle()


def add_chat(bot, updater, args):
    """
    Usage: /accChat chatId
    Result: Adds the chat with "chatId" to the extended functions group.
    """
    if len(args) != 1 or not args[0].lstrip('-').isdigit():
        bot.send_message(chat_id=updater.message.chat_id,
                         text=EnglishStrings.NUMBER_MISSING)
    else:
        EXPANDED_FUNCTION_ACCESS.add_chat_id(int(args[0]))
        bot.send_message(chat_id=updater.message.chat_id,
                         text=EnglishStrings.SUCCESSFUL_ADD)


def echo(bot, updater, args):
    """
    Usage: /echo text
    Result: This will print a message containing "text"
    """
    input_text = updater.message.text
    output_text = " ".join(args)

    bot.send_message(chat_id=updater.message.chat_id,
                     text=output_text)


def chat_id(bot, updater):
    """
    Result: Prints the current chat id.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text=updater.message.chat_id)


def time(bot, updater):
    """
    Result: Prints the current time in preconfigured time zones.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text=ComTime(['Europe/Berlin']).time_message(),
                     parse_mode=ParseMode.MARKDOWN)


def vip(bot, updater):
    """
    Result: Prints how special you are.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text="You are very special!")


def xkcd(bot, updater, args):
    """
    Usage: /xkcd [ number | random ]
    Result: Either the newest xkcd, the xkcd with id "number" or a random xkcd.
    """
    (xkcd_image, xkcd_alt_text) = ComXkcd().get_xkcd(args)
    if xkcd_image is None or xkcd_alt_text is None:
        bot.send_message(chat_id=updater.message.chat_id,
                         text=ComXkcd.WRONG_USAGE)
    else:
        bot.send_photo(chat_id=updater.message.chat_id,
                       photo=xkcd_image,
                       caption=xkcd_alt_text)


def help_me(bot, updater):
    """
    Prints the help message.
    """
    global NORMAL_HELPER
    global EXPANDED_HELPER
    global ADMIN_HELPER

    if RESOURCE_HANDLER.admin_id == updater.message.chat_id:
        bot.send_message(chat_id=updater.message.chat_id,
                         text=ADMIN_HELPER.help_string,
                         parse_mode=ParseMode.MARKDOWN)
    elif EXPANDED_FUNCTION_ACCESS.filter(updater.message):
        bot.send_message(chat_id=updater.message.chat_id,
                         text=EXPANDED_HELPER.help_string,
                         parse_mode=ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=updater.message.chat_id,
                         text=NORMAL_HELPER.help_string,
                         parse_mode=ParseMode.MARKDOWN)


def unkown_command(bot, updater):
    """
    Handles unkown commands send to the bot.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text=EnglishStrings.UNKOWN_COMMAND)


if __name__ == "__main__":
    main()
