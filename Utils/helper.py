"""
This class handles printing the help text for commands
"""
from telegram.ext import CommandHandler


class Helper:
    """
    Class that builds and contains the help text for commands.
    """

    def __init__(self, bot_dispatcher):
        self._help_string = _build_help_string(bot_dispatcher)

    @property
    def help_string(self):
        """
        Returns the help string build during initialization.
        """
        return self._help_string

def _build_help_string(bot_dispatcher):
    """
    Builds the help string from the command string and the functions
    docstring.
    """
    command_handlers = _extract_command_handlers(bot_dispatcher,
                                                 CommandHandler)
    command_help_mapping = _map_commands_to_docstring(command_handlers)
    help_string = _create_help_string_from_map(command_help_mapping)
    return help_string


def _extract_command_handlers(dispatcher, base_type):
    """
    Returns a list of all handlers of a certain base type.
    """
    handlers = []
    for group in dispatcher.handlers:
        handlers.extend(dispatcher.handlers[group])

    selected_handlers = list(filter(lambda handler: isinstance(handler,
                                                               base_type),
                                    handlers))
    return selected_handlers

def _map_commands_to_docstring(command_handlers):
    """
    Returns a mapping of commands to their functions docstrings.
    """
    help_mapping = {}
    for handler in command_handlers:
        command_text = handler.command[0]
        command_help = handler.callback.__doc__.strip()
        help_mapping[command_text] = command_help
    return help_mapping

def _create_help_string_from_map(mapping):
    """
    Returns a string mapping the command to its description
    """
    help_string = ""
    for command in mapping:
        help_string += "{com}: {description}\n".format(com=command,
                                                     description=mapping[command])
    return help_string
