# from src.languages.Ru import MENU_COMMANDS_RU, BOT_MESSAGES_RU
#! Это нужно передавать в конструктор класса, чтобы тот их сеттил
 
#! Этот файл создаётся руками (но было бы хорошо сделать заготовку для класса, только передавать ему тексты)

class Language:
    def __init__(self) -> None:
        # defaults
        self.active_lang = "ru"
        self.set_active_language_to(self.active_lang)
        
        
    def set_active_language_to(self, new_language="ru"):
        if new_language == "ru":
            #! should be loaded to constructor
            # self.commands = MENU_COMMANDS_RU
            # self.messages = BOT_MESSAGES_RU
            pass

    
    def get_active_language(self):
        return self.active_lang
    
    
    def get_commands(self):
        return self.commands
    
    
    def get_messages(self):
        return self.messages
        
        