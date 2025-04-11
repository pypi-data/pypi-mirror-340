from abc import ABC, abstractmethod
import fitz


class Language(ABC):
    """
    Abstract base class for all languages.
    This class is useful to resize the bbox and align the text based on the language.
    I.e. Arabic will be right to left, while English will be left to right.
    """
    # language code property
    @property
    @abstractmethod
    def language_code(self) -> str:
        """
        Returns the language code.
        :return: The language code.
        """
        pass



    # language code property
    @property
    @abstractmethod
    def language_name(self) -> str:
        """
        Returns the language name.
        :return: The language name.
        """
        pass

    # alignment property and setter
    @property
    @abstractmethod
    def alignment(self) -> int:
        """
        Returns the alignment of the language.
        :return: The alignment of the language (left, right).
        """
        pass

    @alignment.setter
    @abstractmethod
    def alignment(self, value: int):
        """
        Sets the alignment of the language.
        :param value: The alignment of the language (left, right, center).
        """
        pass

    def resize_bbox(self, bbox: fitz.Rect, new_width: float) -> fitz.Rect:
        """
        Resizes the bounding box based on the text in the language.
        The bounding box is a tuple of (x, y, width, height).
        """
        # Adjust the bounding box for right-to-left languages

        if self.alignment == fitz.TEXT_ALIGN_RIGHT:
            # For right-to-left languages, move the x-coordinate to the left
            return fitz.Rect(bbox.x1 - new_width , bbox.y0 , bbox.x1 , bbox.y1 )
        elif self.alignment == fitz.TEXT_ALIGN_LEFT:
            # For left-to-right languages, move the x-coordinate to the right
            return fitz.Rect(bbox.x0 + new_width , bbox.y0 , bbox.x1 , bbox.y1 )
        elif self.alignment == fitz.TEXT_ALIGN_CENTER:
            # For center-aligned languages, adjust the x-coordinate to center the text
            center_x = (bbox.x0 + bbox.x1) / 2
            return fitz.Rect(center_x - new_width / 2 , bbox.y0 , center_x + new_width / 2 , bbox.y1 )
        else:
            # If no specific alignment is set, return the original bounding box
            return bbox




class LanguageFactory:
    """
    LanguageFactory is a factory class responsible for creating and managing language objects. 
    It provides methods to create language instances based on their language codes and to list 
    all available languages.
    Methods:
        create(language_code: str) -> Language:
            Factory method to create a language object based on the provided language code.
            If the language code is not supported, raises a ValueError.
        list_languages() -> list:
            Returns a list of all available language names registered in the system.
    Attributes:
        _registery (dict):
            A private dictionary used to cache and store language objects for quick access.
    """

    # A private dictionary to cache language objects
    _registery : 'dict[str , Language]' = {}


    @staticmethod
    def create(language_code: str) -> Language:
        """
        Factory method to create a language object based on the language code.
        :param language_code: The language code.
        :return: The language object.
        """
        # Check if the language code is already registered
        if language_code in LanguageFactory._registery:
            return LanguageFactory._registery[language_code]
        # else iterate through all subclasses of Language
        # and check if the language code matches
        for subclass in Language.__subclasses__():
            # add the subclass to the registry
            LanguageFactory._registery[subclass._language_code] = subclass() # type: ignore
            if subclass._language_code == language_code: # type: ignore
                return subclass()
        raise ValueError(f"Language code {language_code} not supported.")
    

    @staticmethod
    def list_languages() -> 'list[dict[str, str]]':
        """
        Returns a list of all available languages.
        :return: A list of language codes.
        """
        return [{'code' : subclass._language_code , 'name' : subclass._language_name} for subclass in Language.__subclasses__()] # type: ignore
