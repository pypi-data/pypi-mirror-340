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
    _language_instance = None

    active_lang: str
    commands: dict[str, str]
    bot_messages: dict[str, str]

    def __new__(cls, menu_commands: dict[str, str], bot_messages: dict[str, str]):
        if cls._language_instance is None:
            cls._language_instance = super().__new__(cls)
            cls._language_instance.active_lang = DEFAULT_LANGUAGE
            cls._language_instance.commands = menu_commands
            cls._language_instance.messages = bot_messages

        return cls._language_instance

    def __init__(self) -> None:
        pass

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
