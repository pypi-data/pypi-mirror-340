from os import getenv

if getenv("ENVIRONMENT") == "testing":
    from data.env import DEFAULT_LANGUAGE

else:
    from bot_engine.data.env import DEFAULT_LANGUAGE


class Language:
    """
    Sets the default language from the .env on the creation.
    Changes language through method, if needed
    """

    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def __init__(
        self, menu_commands: dict[str, str] = None, bot_messages: dict[str, str] = None
    ):
        if not self.__class__._is_initialized:
            if menu_commands is None or bot_messages is None:
                raise ValueError("🔴 First 'Language' class initialization requires commands and messages")

            self.active_lang = DEFAULT_LANGUAGE
            self.commands = menu_commands
            self.messages = bot_messages
            self.__class__._is_initialized = True

    def change_language(self, new_language: str, new_commands, new_messages):
        self.active_lang = new_language
        self.commands = new_commands
        self.messages = new_messages

    def get_active_language(self):
        return self.active_lang

    def get_commands(self):
        return self.commands

    def get_messages(self):
        return self.messages
