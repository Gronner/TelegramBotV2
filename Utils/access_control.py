"""
Collection of utilities allowing to control which chats can access which
commands.
"""
import pickle
import os
from telegram.ext import filters

class AccessControlFilter(filters.BaseFilter):
    """
    Restricts access to commands by querying against a white list.
    """

    def __init__(self, white_list_path):
        self.white_list_path = white_list_path
        self.white_list = self._read_white_list()

    def filter(self, message):
        """
        Checks wether the messages chat id is part of the white list.
        """
        return message.chat_id in self.white_list

    def _read_white_list(self):
        """
        Deserializes the white list.
        """
        if not os.path.isfile(self.white_list_path):
            return []
        with open(self.white_list_path, 'rb') as white_list_file:
            return pickle.load(white_list_file)

    def add_chat_id(self, chat_id):
        """
        Adds a chat ID to the filters whitelist.
        """
        if chat_id in self.white_list:
            return
        self.white_list.append(chat_id)
        with open(self.white_list_path, 'wb') as white_list_file:
            pickle.dump(self.white_list, white_list_file)
