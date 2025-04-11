"""
This module initializes the languages subpackage, making its components accessible.

It imports and makes available key classes for different languages and the LanguageFactory.
"""
__all__ = [
    "Language",
    "Arabic",
    "Turkish",
    "LanguageFactory",
    "English",
    "French"
]

from pdflator.languages.language import Language
from pdflator.languages.turkish import Turkish
from pdflator.languages.arabic import Arabic
from pdflator.languages.language import LanguageFactory
from pdflator.languages.english import English
from pdflator.languages.french import French