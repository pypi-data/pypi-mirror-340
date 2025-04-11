import asyncio

from pdflator.translation.translator import Translator
from googletrans import Translator as GTranslator
from pdflator.languages import Language as BaseLanguage

class GoogleTranslator(Translator):
    """
    GoogleTranslator class that implements the Translator interface.
    Uses the googletrans library to translate text.
    """

    _translator_code = "gtrans"
    _translator_name = "Google Translate API"

    def __repr__(self):
        """
        Returns a string representation of the GoogleTranslator object.
        :return: A string representation of the GoogleTranslator object.
        """
        return "GoogleTranslator(Google Translate API)"
    
    def __str__(self):
        """
        Returns a string representation of the GoogleTranslator object.
        :return: A string representation of the GoogleTranslator object.
        """
        return "GoogleTranslator(Google Translate API)"
    
    @property
    def translator_name(self) -> str:
        """
        Returns the translator name.
        :return: The translator name.
        """
        return self._translator_name


    @property
    def translator_code(self) -> str:
        """
        Returns the translator code.
        :return: The translator code.
        """
        return self._translator_code

    def detect_lang(self,input_text : str) -> str:
        """
        Detect the language of the input text using Google Translate API.
        """
        return asyncio.run(self._detect_lang(input_text))

    def translate(self,input_text: str , dest_lang : BaseLanguage) -> str:
        """
        Translate the input text to the specified destination language using Google Translate API.
        since googletrans is async this function acts as a wrapper for the async function to standardize the interface
        """
        return asyncio.run(self._translate(input_text, dest_lang.language_code))
    
    async def _translate(self,text : str , dest_lang : str = "en") -> str:
        """
        Since googletrans is async we need to use async with to translate the text
        """
        async with GTranslator() as translator:
            try:
                result = await translator.translate(text, dest=dest_lang)
                return result.text
            except Exception as e:
                print(f"Translation error: {e}")
                return text
                # Fallback to original text


    async def _detect_lang(self,text : str):
        """
        Detects the language of the input text using Google Translate API.
        """
        async with GTranslator() as translator:
            result = await translator.detect(text)
        if result.confidence < 0.5:
            raise ValueError("Language detection confidence is low.")
        return result.lang