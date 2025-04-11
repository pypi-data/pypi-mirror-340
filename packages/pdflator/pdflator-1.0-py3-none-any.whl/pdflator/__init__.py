"""
This module initializes the pdf_translator package, making its components accessible.

It imports and makes available key classes and modules for language handling and translation.
"""
__all__ = [
    "GoogleTranslator",
    "Translator",
    "Arabic",
    "Turkish",
    "Language",
    "LanguageFactory",
    "TranslatorFactory",
    "main",
    "English",
    "French",
    "LibreTranslator",
]

# Explicit absolute imports

# Translation imports
from pdflator.translation.translator import TranslatorFactory
from pdflator.translation.translator import Translator
from pdflator.translation.google_translator import GoogleTranslator
from pdflator.translation.libretranslate_translator import LibreTranslator


# Language imports
from pdflator.languages.language import LanguageFactory
from pdflator.languages.language import Language
from pdflator.languages.arabic import Arabic
from pdflator.languages.turkish import Turkish
from pdflator.languages.english import English
from pdflator.languages.french import French



# Main module import
from pdflator.main import main