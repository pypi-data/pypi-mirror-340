from abc import ABC, abstractmethod
from pdflator.languages import Language


class Translator(ABC):
    """
    Abstract base class for all translators.
    """

    @property
    @abstractmethod
    def translator_code(self) -> str:
        """
        Returns the translator code.
        :return: The translator code.
        """
        pass

    @property
    @abstractmethod
    def translator_name(self) -> str:
        """
        Returns the translator name.
        :return: The translator name.
        """
        pass

    @abstractmethod
    def detect_lang(self,input_text : str) -> str:
        """
        Detects the language of the input text.
        :param input_text: The text to detect the language of.
        :return: The language code of the input text.
        """
        pass

    @abstractmethod
    def translate(self,input_text: str , dest_lang : Language) -> str:
        """
        Translates the input text to the specified destination language.
        :param input_text: The text to translate.
        :param dest_lang: The destination language.
        :return: The translated text.
        """
        pass



class TranslatorFactory:
    """
    TranslatorFactory is a factory class responsible for creating and managing translator objects.
    """

    _registery : 'dict[str, Translator]' = {}

    @staticmethod
    def create(translator : str) -> Translator:
        """
        Create an instance of a Translator class based on the provided language.
        
        :param translator: The name of the translator class to create.
        :return: An instance of the specified Translator class.
        :raises ValueError: If the translator is unknown.
        """
        # Check if the translator is already registered
        if translator in TranslatorFactory._registery:
            return TranslatorFactory._registery[translator]
        # If not, dynamically create an instance of the translator class
        for subclass in Translator.__subclasses__():
            # add the subclass to the registery
            TranslatorFactory._registery[subclass._translator_code] = subclass() # type: ignore
            if subclass._translator_code == translator: # type: ignore
                return subclass()
        raise ValueError(f"Unknown translator: {translator}")
        
    @staticmethod
    def list_translators() -> 'list[dict[str,str]]':
        """
        Returns a list of all available translators.
        
        :return: A list of translator codes.
        """
        return [{'code' : subclass._translator_code , 'name' : subclass._translator_name} for subclass in Translator.__subclasses__()]