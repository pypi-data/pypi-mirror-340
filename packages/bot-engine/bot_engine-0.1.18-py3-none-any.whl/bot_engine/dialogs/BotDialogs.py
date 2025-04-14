from os import getenv

if getenv("ENVIRONMENT") == "testing":
    from bot.Bot import Bot
    from dialogs.DialogGenerator import DialogGenerator
    from languages.Language import Language

else:
    from bot_engine.bot.Bot import Bot
    from bot_engine.dialogs.DialogGenerator import DialogGenerator
    from bot_engine.languages.Language import Language


class BotDialogs:
    def __init__(self):
        """
            Зависимости, которые было у меня ранее: 
            1. Бот
            2. Генератор диалогов
            3. И тексты
            
        """
        self.Bot = Bot()
        self.DialogGenerator = DialogGenerator()
        self.messages = Language().messages    


    def set_dialogs(self):
        """ 
            Use self.dialog_generator to generate dialogs.
            For example: 
            
            self.DialogGenerator.make_dialog(...)  
        """
        pass
