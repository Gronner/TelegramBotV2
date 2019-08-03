"""
This module provides filters for simple edge cases.
"""
from telegram.ext import filters

class UnkownCommandHandler(filters.BaseFilter):
    """
    This filter avoids to trigger the unkown command handler when the command
    can be found in another group.
    The filter must be instanciated after the last command to be used with
    the unkown file handler.
    """

    def __init__(self, dispatcher, groups, combined_filter=None):
        self._dispatcher = dispatcher
        self._groups = groups
        self.combined_filter = combined_filter
        self.commands = self._get_commands()

    def _get_commands(self):
        """
        Get all commands from the specified groups.
        """
        handlers = []
        for group in self._groups:
            handlers.extend(self._dispatcher.handlers[group])
        commands = []
        for handler in handlers:
            for command in handler.command:
                commands.append(command)
        return commands

    def filter(self, message):
        """
        Checks wether a command send to the bot is a valid command for this
        bot.
        """
        full_message = message.text
        if not full_message.startswith('/'):
            return False
        command_message = full_message.lstrip('/').split(' ')[0].lower()
        if command_message not in self.commands:
            return self._additional_filter(message)
        return False

    def _additional_filter(self, message):
        """
        Handles an additional filter.
        """
        if self.combined_filter is None:
            return True
        else:
            return self.combined_filter.filter(message)
