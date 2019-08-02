"""
Handler class for external resources used by the bot.
"""

class ResourceManager:
    """
    Handler class for external resources used by the bot.
    """

    def __init__(self, token, admin_id):
        self._token = token
        self._admin_id = admin_id

    @property
    def token(self):
        """
        Allows read access to the token.
        """
        return self._token

    @property
    def admin_id(self):
        """
        Allows read access to the admin id.
        """
        return self._admin_id
