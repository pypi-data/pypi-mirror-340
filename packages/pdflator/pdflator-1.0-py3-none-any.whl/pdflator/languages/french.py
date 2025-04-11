from pdflator.languages.language import Language
import fitz

class French(Language):
    """
    French language class.
    This class is useful to resize the bbox and align the text based on the language.
    I.e. Arabic will be right to left, while English will be left to right.

    French is a left-to-right language, so the alignment is set to left by default.
    """
    _language_name = "French"
    _language_code = "fr"
    _alignment = fitz.TEXT_ALIGN_LEFT  # default alignment for Turkish



    def __repr__(self):
        """
        Returns a string representation of the French object.
        :return: A string representation of the French object.
        """
        return self.__str__()
    def __str__(self):
        """
        Returns a string representation of the French object.
        :return: A string representation of the French object.
        """
        return f"French(language_code={self.language_code}, alignment={self._alignment})"
    

    
    @property
    def language_code(self) -> str:
        """
        Returns the language code.
        :return: The language code.
        """
        return self._language_code


    @property
    def alignment(self) -> int:
        """
        Returns the alignment of the language.
        :return: The alignment of the language (left, right).
        """
        return self._alignment
    
    @alignment.setter
    def alignment(self, value: int):
        """
        Sets the alignment of the language.
        :param value: The alignment of the language (left, right).
        """
        if value not in (fitz.TEXT_ALIGN_LEFT, fitz.TEXT_ALIGN_RIGHT , fitz.TEXT_ALIGN_CENTER):
            raise ValueError("Alignment must be either left or right or center.")
        self._alignment = value

    @property
    def language_name(self):
        """
        Returns the language name.
        :return: The language name.
        """
        return self._language_name

