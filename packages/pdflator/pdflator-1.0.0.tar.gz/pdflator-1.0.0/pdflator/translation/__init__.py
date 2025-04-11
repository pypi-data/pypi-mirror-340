"""
This module initializes the translation subpackage, making its components accessible.

It imports and makes available key classes for different translators and the TranslatorFactory.
"""
__all__ = [
    "Translator",
    "GoogleTranslator",
    "TranslatorFactory",
    "LibreTranslator",
    ]


from pdflator.translation.google_translator import GoogleTranslator
from pdflator.translation.translator import Translator
from pdflator.translation.translator import TranslatorFactory
from pdflator.translation.libretranslate_translator import LibreTranslator
