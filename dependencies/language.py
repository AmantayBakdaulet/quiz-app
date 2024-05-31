from fastapi import Header


SUPPORTED_LANGUAGES = ["en", "es", "pt", "de", "tr", "fr"]

def get_language(accept_language: str = Header(None)):
    if accept_language:
        preferred_language = accept_language.split(",")[0].split(";")[0]
        if preferred_language in SUPPORTED_LANGUAGES:
            return preferred_language
    return "en"
