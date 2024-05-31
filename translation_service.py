from typing import Any, Dict 

from deep_translator import GoogleTranslator


class TranslationService:

    def __init__(self) -> None:
        pass

    def translate_str(self, source: str = 'auto', target: str = 'es', content: str = 'Hello!') -> str:
        return GoogleTranslator(source=source, target=target).translate(content)

    def translate_dict(self, source: str = 'auto', target: str = 'es', content: Dict[str, Any] = {}) -> Dict[str, Any]:
        translated_dict = {}
        for key, value in content.items():
            if isinstance(value, dict):
                translated_dict[key] = self.translate_dict(source, target, value)
            elif isinstance(value, str):
                translated_dict[key] = self.translate_str(source, target, value)
            else:
                translated_dict[key] = value
        return translated_dict
