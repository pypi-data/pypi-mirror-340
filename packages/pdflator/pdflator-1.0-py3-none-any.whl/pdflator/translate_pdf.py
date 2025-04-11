# TODO: Add support for batch translation for faster processing

from pdflator.languages import LanguageFactory
from pdflator.translation import TranslatorFactory
from pdflator.translation import Translator

import fitz
import os
from dotenv import load_dotenv

load_dotenv()

OUTPUT_FONT_SIZE = int(os.getenv("OUTPUT_FONT_SIZE", 12))
REDACTION_COLOR = tuple(map(int, os.getenv("REDACTION_COLOR", "(1,1,1)").strip("()").split(",")))
SCALING_FACTOR = float(os.getenv("SCALING_FACTOR", 0.75))

def translate_pdf(input_path : str, output_path : str,input_lang : str = 'auto' , dest_lang : str ='en', translator_code : str = 'gtrans') -> None:
    """
    Translate a PDF file while preserving its layout.

    This function translates the text content of a PDF file from a source language to a target language.
    It preserves the original layout of the PDF, including text positioning.

    :param input_path: Path to the input PDF file to be translated.
    :type input_path: str
    :param output_path: Path to save the translated PDF file.
    :type output_path: str
    :param input_lang: Language code of the input PDF text. Defaults to 'auto' for automatic detection.
    :type input_lang: str, optional
    :param dest_lang: Language code for the target translation language. Defaults to 'en' (English).
    :type dest_lang: str, optional
    :param translator_code: Translator code to use for translation. Defaults to 'gtrans'.
    :type translator_code: str, optional

    :raises FileNotFoundError: If the input PDF file does not exist.
    :raises ValueError: If the translation process encounters invalid input or unsupported languages.

    :note:
        - The function uses a translator dynamically created by the `TranslatorFactory`.
        - The layout of the PDF is preserved by extracting text blocks and re-inserting translated text.
        - Font resizing and bounding box adjustments are performed to ensure translated text fits within the original layout.

    :example:
        translate_pdf(
            input_path="/path/to/input.pdf",
            output_path="/path/to/output.pdf",
            input_lang="auto",
            dest_lang="fr",
            translator_code = 'gtrans')
    """

    
    translator : Translator = TranslatorFactory.create(translator_code)
    doc : fitz.Document = fitz.open(input_path)
    if dest_lang == 'auto':
          raise ValueError("Destination language cannot be 'auto'. Please specify a valid language code.")
    final_lang = LanguageFactory.create(dest_lang)

    if input_lang == 'auto':
        # Detect the language of the input PDF
        # get the text from the first page and use it to detect the language
        try:
            detected_lang = translator.detect_lang(doc[0].get_text("text"))
            input_lang = detected_lang
        except Exception as e:
            print(f"Error detecting language: {e}")
            input_lang = 'en' # Default to English if detection fails
    initial_lang = LanguageFactory.create(input_lang)

    for page in doc:
        # Extract text information with metadata
        # * We are using extractBLOCKS() to capture full sentences rather than words so we don't lose context while translating
        blocks = page.get_textpage().extractBLOCKS()
        translation_list = []
        for block in blocks:

                        # if block type is not "text block" just pass that block
                        if block[6] != 0:
                             continue
                        # Extract text and formatting information
                        original_text = block[4]
                        bbox = fitz.Rect(block[0],block[1],block[2],block[3])  # Text insertion point
                        # Get original font or use custom font
                        current_font = fitz.Font('notosbo')
                        # Translate text
                        translated_text = translator.translate(original_text, dest_lang=final_lang)

                        # get longest sentence
                        longest_sentence = max(translated_text.split('\n') , key=len)

                        # get the new text width
                        try:
                            page.add_redact_annot(bbox,'.',text_color=REDACTION_COLOR)
                            new_width : float = fitz.get_text_length(text = longest_sentence,fontsize= OUTPUT_FONT_SIZE * SCALING_FACTOR) # TODO: get the fixed font size from the user input
                            new_width = new_width * 1.2 # padding

                            bbox = initial_lang.resize_bbox(bbox, new_width) if new_width > 0 else bbox

                            translation_list.append({
                                'bbox' : bbox,
                                'text': translated_text,
                                'font': current_font,
                            })
                        except Exception as e:
                            print(f"Error processing block: {e}")


        try:
            page.apply_redactions(images=True)
        except Exception as e:
            print(f"Error applying redactions: {e}")

        # Insert translated text
        for item in translation_list:
            shrink_factor = 0.95
            # keep trying and shrink the font until fits
            while True:
                try:
                    result = page.insert_textbox(
                        rect=item['bbox'],
                        buffer=item['text'],
                        fontsize=OUTPUT_FONT_SIZE * SCALING_FACTOR * shrink_factor,
                        rotate=0,  # Preserve original rotation
                        align = initial_lang.alignment,
                    )
                    if result > 0 :
                         break
                except Exception as e:
                    print(f"Error inserting textbox: {e}")
                    break # Exit the inner loop if there's an error
                shrink_factor -= 0.1


    # Save translated PDF
    try:
        doc.save(output_path)
        print(f"Successfully translated PDF saved to {output_path}")
    except Exception as e:
        print(f"Error saving PDF: {e}")