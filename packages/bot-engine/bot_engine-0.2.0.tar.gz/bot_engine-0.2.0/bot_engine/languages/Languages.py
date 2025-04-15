from dataclasses import dataclass, field
from Locale import Locale
from typing import ClassVar


@dataclass
class Languages:
    active_lang: str = "ru"
    languages: ClassVar[dict[str, Locale]] = {}

    def add_locale(self, locale: Locale):
        self.languages[locale.language] = locale

    def get_active_locale(self) -> Locale | None:
        return self.languages.get(self.active_lang)

    def get_messages(self, user_language: str | None = None) -> list[dict[str, str]]:
        active_language = user_language or self.active_lang
        locale = self.languages.get(active_language)

        if not locale:
            raise ValueError(f"Locale '{active_language}' not found.")
        
        return locale.messages

