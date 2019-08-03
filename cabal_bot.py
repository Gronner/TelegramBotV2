"""
Runner for the C.A.B.A.L. Telegram Bot.
"""
from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from Commands import ComTime, ComXkcd
from ResourceManager.resource_manager import ResourceManager
from StringConstants.string_constants import EnglishStrings
from Utils import access_control, file_reader, helper, filters

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
    EXPANDED_FUNCTION_ACCESS.add_chat_id(RESOURCE_HANDLER.admin_id)

    updater = Updater(RESOURCE_HANDLER.token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_me))
    dispatcher.add_handler(CommandHandler("echo", echo, pass_args=True))
    dispatcher.add_handler(CommandHandler("id", get_chat_id))
    dispatcher.add_handler(CommandHandler("time", time))
    dispatcher.add_handler(CommandHandler("xkcd", xkcd, pass_args=True))
    dispatcher.add_handler(CommandHandler("remind", set_timer,
                                          pass_args=True,
                                          pass_job_queue=True,
                                          pass_chat_data=True))
    dispatcher.add_handler(CommandHandler("unremind", unset_timer,
                                          pass_args=True,
                                          pass_chat_data=True))

    dispatcher.add_handler(CommandHandler("vip",
                                          vip,
                                          filters=EXPANDED_FUNCTION_ACCESS),
                           group=1)

    dispatcher.add_handler(CommandHandler("addChat",
                                          add_chat,
                                          pass_args=True,
                                          filters=admin_only),
                           group=666)

    normal_unkown_filter = filters.UnkownCommandHandler(dispatcher, [0])
    expanded_unkown_filter = filters.UnkownCommandHandler(dispatcher,
                                                          [0, 1],
                                                          EXPANDED_FUNCTION_ACCESS)
    admin_unkown_filter = filters.UnkownCommandHandler(dispatcher,
                                                       [0, 1, 666],
                                                       admin_only)
    dispatcher.add_handler(MessageHandler(admin_unkown_filter,
                                          unkown_command),
                           group=999)
    dispatcher.add_handler(MessageHandler(admin_only, skip), group=999)
    dispatcher.add_handler(MessageHandler(expanded_unkown_filter,
                                          unkown_command),
                           group=999)
    dispatcher.add_handler(MessageHandler(EXPANDED_FUNCTION_ACCESS, skip),
                           group=999)
    dispatcher.add_handler(MessageHandler(normal_unkown_filter,
                                          unkown_command),
                           group=999)

    NORMAL_HELPER = helper.Helper(dispatcher)
    EXPANDED_HELPER = helper.Helper(dispatcher, [0, 1])
    ADMIN_HELPER = helper.Helper(dispatcher, [0, 1, 666])

    updater.start_polling()
    updater.idle()


def add_chat(bot, updater, args):
    """
    Usage: /accChat <chatId>
    Result: Adds the chat with "chatId" to the extended functions group.
    """
    if len(args) != 1 or not args[0].lstrip('-').isdigit():
        bot.send_message(chat_id=updater.message.chat_id,
                         text=EnglishStrings.NUMBER_MISSING)
    else:
        EXPANDED_FUNCTION_ACCESS.add_chat_id(int(args[0]))
        bot.send_message(chat_id=updater.message.chat_id,
                         text=EnglishStrings.SUCCESSFUL_ADD)


def get_chat_id(bot, updater):
    """
    Result: Prints the current chat id.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text=updater.message.chat_id)


def echo(bot, updater, args):
    """
    Usage: /echo <text>
    Result: This will print a message containing "text"
    """
    output_text = " ".join(args)

    bot.send_message(chat_id=updater.message.chat_id,
                     text=output_text)


def set_timer(bot, updater, args, job_queue, chat_data):
    """
    Usage: /remind <id> <hours> <minutes> <text>
    Result: This will print a reminder, if specified with "text" as output,
    after hours:minutes have passed.
    """
    print(len(args))
    if len(args) < 4 or not args[1].isdigit() or not args[2].isdigit():
        bot.send_message(chat_id=updater.message.chat_id,
                         text="Usage: /remind <id> <hours> <minutes> [<text>]")
        return

    job_context = {}
    timer_id = args[0]
    hours = int(args[1])
    minutes = int(args[2])
    job_context['text'] = ' '.join(args[3:])
    job_context['chat'] = updater.message.chat_id

    chat_data['jobs' + timer_id] = job_queue.run_once(_print_reminder,
                                                      hours * 3600 + minutes * 60,
                                                      context=job_context)

    updater.message.reply_text("Timer was set successfully!")


def _print_reminder(bot, job):
    """
    Responsible for executing the reminder job.
    """
    chat_id = job.context['chat']
    output_text = job.context['text']
    bot.send_message(chat_id=chat_id,
                     text=output_text)


def time(bot, updater):
    """
    Result: Prints the current time in preconfigured time zones.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text=ComTime(['Europe/Berlin']).time_message(),
                     parse_mode=ParseMode.MARKDOWN)


def unset_timer(bot, updater, args, chat_data):
    """
    Usage: /unremind <id>
    Result: Will stop the reminder with id "id" from being executed."
    """
    if not args:
        bot.send_message(chat_id=updater.message.chat_id,
                         text="Usage: /unremind <id>, id must be a number")
        return
    job_id = "jobs" + args[0]
    if job_id  not in chat_data:
        bot.send_message.reply_text("No reminder of that id")
        return
    job = chat_data[job_id]
    job.schedule_removal()
    del chat_data[job_id]
    bot.send_message.reply_text("Reminder disabled")


def vip(bot, updater):
    """
    Result: Prints how special you are.
    """
    bot.send_message(chat_id=updater.message.chat_id,
                     text="You are very special!")


def xkcd(bot, updater, args):
    """
    Usage: /xkcd [ <number> | random ]
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
                     text=EnglishStrings.UNKOWN_COMMAND + "0")


def skip(bot, updater):
    """
    Used to catch unwanted fall_throughs.
    """
    pass


if __name__ == "__main__":
    main()
