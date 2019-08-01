"""
Handler class for external resources used by the bot.
"""

class ResourceManager:
    """
    Handler class for external resources used by the bot.
    """

    def __init__(self, token):
        self._token = token

    @property
    def token(self):
        """
        Allows read access to the token.
        """
        return self._token
