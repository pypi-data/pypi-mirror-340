import asyncio
import os # Import os
from dotenv import load_dotenv # Import load_dotenv

from pdflator.translation.translator import Translator
from libretranslatepy import LibreTranslateAPI
from pdflator.languages import Language as BaseLanguage

# Load environment variables from the project root .env file
# Assuming the .env file is two levels up from this file's directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

class LibreTranslator(Translator):
    """
    GoogleTranslator class that implements the Translator interface.
    Uses the googletrans library to translate text.
    """

    _translator_code = "libre"
    _translator_name = "LibreTranslate API" # Updated name slightly


    def __init__(self):
        """
        Initializes the LibreTranslator object using the API URL from environment variables.
        """
        # Read the single API URL parameter
        api_url = os.getenv("LIBRE_TRANSLATE_API", 'http://localhost:8000/') # Default if not found

        self._translator = LibreTranslateAPI(api_url)

    def __repr__(self):
        """
        Returns a string representation of the GoogleTranslator object.
        :return: A string representation of the GoogleTranslator object.
        """
        return "LibreTranslator(Libre Translate API)"
    
    def __str__(self):
        """
        Returns a string representation of the GoogleTranslator object.
        :return: A string representation of the GoogleTranslator object.
        """
        return "LibreTranslator(Libre Translate API)"
    
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
        result : list[dict] = self._translator.detect(input_text)
        if result[0]['confidence'] < 0.5:
            raise ValueError("Language detection confidence is low.")
        
        return result[0]['language']

    def translate(self,input_text: str , dest_lang : BaseLanguage) -> str:
        """
        Translate the input text to the specified destination language using LibreTranslate API.
        """
        # The original comment mentioned googletrans async, which is incorrect for LibreTranslate
        return self._translator.translate(input_text, "auto", dest_lang.language_code) # Added source lang "auto"