from googletrans import Translator
import asyncio
from OctoLingo.utils import split_text_into_chunks, cache_translation
from OctoLingo.exceptions import TranslationError
from OctoLingo.ocr import OctoOCR
from OctoLingo.file_handler import FileHandler
import re


class OctoLingo:
    def __init__(self, ocr_languages=['en'], ocr_gpu=False):
        """
        Initialize the translator with Google Translate as the default provider.
        
        :param ocr_languages: List of languages for OCR (default: ['en'])
        :param ocr_gpu: Whether to use GPU for OCR (default: False)
        """
        self.translator = Translator()
        self.ocr = OctoOCR(languages=ocr_languages, gpu=ocr_gpu)
        
    def validate_language(self, language_code):
        """Validate if the target language is supported by the translation API."""
        supported_languages = ['ab', 'ace', 'ach', 'af', 'sq', 'alz', 'am', 'ar', 'hy', 'as', 'awa', 'ay', 'az', 'ban', 'bm','ba', 'eu', 'btx', 'bts', 'bbc', 'be', 'bem', 'bn', 'bew', 'bho', 'bik', 'bs', 'br', 'bg', 'bua', 'yue', 'ca', 'ceb', 'ny', 'zh', 'zh-CN', 'zh-TW', 'cv','co','crh','hr', 'cs', 'da','din', 'dv', 'doi', 'dov', 'nl', 'dz', 'en', 'eo', 'et', 'ee', 'fj', 'fil','tl', 'fi', 'fr','fr-FR', 'fr-CA', 'fy', 'ff', 'gaa', 'gl', 'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'cnh', 'ha', 'haw', 'iw', 'he', 'hil', 'hi', 'hmn', 'hu', 'hrx', 'is', 'ig', 'ilo', 'id', 'ga', 'it', 'ja', 'jw', 'jv', 'kn', 'pam', 'kk', 'km', 'cgg', 'rw', 'ktu', 'gom', 'ko', 'kri', 'ku', 'ckb', 'ky', 'lo', 'ltg', 'la', 'lv', 'lv', 'lij', 'li', 'ln', 'lt', 'lmo', 'luo', 'lb', 'mk', 'mai', 'mak', 'mg', 'ms', 'ms-Arab', 'ml', 'mt' , 'mi', 'mr', 'chm', 'mni-Mtei', 'min', 'lus', 'mn', 'my', 'nr', 'new', 'ne', 'nso', 'no', 'nus', 'oc', 'or', 'om', 'pag', 'pap', 'ps', 'ps', 'fa', 'pl', 'pt', 'pt-PT', 'pt-BR', 'pa', 'pa-Arab', 'qu', 'rom', 'ro', 'rn', 'ru', 'sm', 'sg', 'sa', 'gd', 'sr', 'st', 'crs', 'shn', 'sn', 'scn', 'szl', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'ss', 'sv', 'tg', 'ta', 'tt', 'te', 'tet', 'th', 'ti', 'ts','tn', 'tr', 'tk', 'ak', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu', 'yua'] 
        if language_code not in supported_languages:
            raise TranslationError(f"Unsupported language: {language_code}")
        return True

    def detect_language(self, text):
        """Detect the language of the input text."""
        try:
            detection = self.translator.detect(text)
            confidence = detection.confidence if detection.confidence is not None else 0.0
            return detection.lang, confidence
        except Exception as e:
            raise TranslationError(f"Language detection failed: {str(e)}")
    
    def _is_binary_data(self, data):
        """Check if data appears to be binary"""
        if isinstance(data, bytes):
            return True
        if isinstance(data, str):
            if any(ord(char) > 127 for char in data[:1000]):
                return True
        return False

    def _clean_translation_result(self, result):
        """Validate and clean translation result"""
        if not hasattr(result, 'text'):
            raise TranslationError("Invalid translation response")
        
        text = result.text
        if self._is_binary_data(text):
            raise TranslationError("Translation returned binary data")
            
        # Basic cleaning
        text = re.sub(r'[\x00-\x1f\x7f-\xff]', '', text)
        return text.strip()

    @cache_translation
    def translate(self, text, dest_language, src_language='auto', max_retries=3):
        """
        Translate text to the target language.
        :param text: Input text to translate.
        :param dest_language: Target language code (e.g., 'es' for Spanish).
        :param src_language: Source language code (default: 'auto' for auto-detection).
        :param max_retries: Maximum number of retries for failed translations.
        :return: Translated text and confidence score.
        """
        self.validate_language(dest_language)
        # Validate and clean input text
        if not text or not isinstance(text, str):
            raise TranslationError("Invalid text input for translation")
            
        text = self._clean_text(text)
        if not text:
            raise TranslationError("Text is empty after cleaning")
        
        if self._is_binary_data(text):
            raise TranslationError("Cannot translate binary data")
        
        chunks = split_text_into_chunks(text)
        translated_chunks = []

        for chunk in chunks:
            for attempt in range(max_retries):
                try:
                    translated = self.translator.translate(chunk, dest=dest_language, src=src_language)
                    clean_text = self._clean_translation_result(translated)
                    translated_chunks.append(clean_text)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise TranslationError(f"Translation failed after {max_retries} retries: {str(e)}")

        return " ".join(translated_chunks), 1.0  # Confidence score is always 1.0 for now

    async def translate_async(self, text, dest_language, src_language='auto', max_retries=3):
        """Asynchronously translate text to the target language."""
        return await asyncio.get_event_loop().run_in_executor(
            None, self.translate, text, dest_language, src_language, max_retries
        )

    def translate_batch(self, texts, dest_language, src_language='auto', max_retries=3):
        """
        Translate a batch of texts to the target language.
        :param texts: List of input texts to translate.
        :param dest_language: Target language code.
        :param src_language: Source language code (default: 'auto').
        :param max_retries: Maximum number of retries for failed translations.
        :return: List of translated texts and confidence scores.
        """
        return [self.translate(text, dest_language, src_language, max_retries) for text in texts]

    def translate_file(self, file_path, dest_language, src_language='auto', max_retries=3):
        """
        Translate text from a file (supports text files, images, and PDFs with OCR).
        
        :param file_path: Path to the input file
        :param dest_language: Target language code
        :param src_language: Source language code (default: 'auto')
        :param max_retries: Maximum number of retries for failed translations
        :return: Translated text and confidence score
        """
        try:
            # First try to read as plain text
            try:
                text = FileHandler.read_file(file_path)
                if self._is_binary_data(text):
                    raise TranslationError("File contains binary data")
            except (UnicodeDecodeError, TranslationError):
                # If text reading fails, try OCR
                text = self.ocr.extract_text(file_path)
            
            # Clean and validate extracted text
            text = self._clean_text(text)
            if not text:
                raise TranslationError("No valid text could be extracted from the file")
                
            return self.translate(text, dest_language, src_language, max_retries)
        except Exception as e:
            raise TranslationError(f"File translation failed: {str(e)}")

    async def translate_file_async(self, file_path, dest_language, src_language='auto', max_retries=3):
        """Asynchronously translate text from a file."""
        return await asyncio.get_event_loop().run_in_executor(
            None, self.translate_file, file_path, dest_language, src_language, max_retries
        )
    
    def _clean_text(self, text):
        """Thoroughly clean text to prevent corruption"""
        if not isinstance(text, str):
            try:
                text = str(text, 'utf-8', errors='replace')
            except:
                text = str(text)
                
        # Remove non-printable characters
        text = ''.join(char for char in text if char.isprintable() or char in {'\n', '\t', '\r'})
        
        # Remove binary artifacts and corrupted sequences
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\xff]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text














# from googletrans import Translator
# import asyncio
# from OctoLingo.utils import split_text_into_chunks, cache_translation
# from OctoLingo.exceptions import TranslationError

# class OctoLingo:
#     def __init__(self):
#         """Initialize the translator with Google Translate as the default provider."""
#         self.translator = Translator()

#     def validate_language(self, language_code):
#         """Validate if the target language is supported by the translation API."""
#         # Hardcode supported languages for now
#         supported_languages = ['ab', 'ace', 'ach', 'af', 'sq', 'alz', 'am', 'ar', 'hy', 'as', 'awa', 'ay', 'az', 'ban', 'bm','ba', 'eu', 'btx', 'bts', 'bbc', 'be', 'bem', 'bn', 'bew', 'bho', 'bik', 'bs', 'br', 'bg', 'bua', 'yue', 'ca', 'ceb', 'ny', 'zh', 'zh-CN', 'zh-TW', 'cv','co','crh','hr', 'cs', 'da','din', 'dv', 'doi', 'dov', 'nl', 'dz', 'en', 'eo', 'et', 'ee', 'fj', 'fil','tl', 'fi', 'fr','fr-FR', 'fr-CA', 'fy', 'ff', 'gaa', 'gl', 'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'cnh', 'ha', 'haw', 'iw', 'he', 'hil', 'hi', 'hmn', 'hu', 'hrx', 'is', 'ig', 'ilo', 'id', 'ga', 'it', 'ja', 'jw', 'jv', 'kn', 'pam', 'kk', 'km', 'cgg', 'rw', 'ktu', 'gom', 'ko', 'kri', 'ku', 'ckb', 'ky', 'lo', 'ltg', 'la', 'lv', 'lv', 'lij', 'li', 'ln', 'lt', 'lmo', 'luo', 'lb', 'mk', 'mai', 'mak', 'mg', 'ms', 'ms-Arab', 'ml', 'mt' , 'mi', 'mr', 'chm', 'mni-Mtei', 'min', 'lus', 'mn', 'my', 'nr', 'new', 'ne', 'nso', 'no', 'nus', 'oc', 'or', 'om', 'pag', 'pap', 'ps', 'ps', 'fa', 'pl', 'pt', 'pt-PT', 'pt-BR', 'pa', 'pa-Arab', 'qu', 'rom', 'ro', 'rn', 'ru', 'sm', 'sg', 'sa', 'gd', 'sr', 'st', 'crs', 'shn', 'sn', 'scn', 'szl', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'ss', 'sv', 'tg', 'ta', 'tt', 'te', 'tet', 'th', 'ti', 'ts','tn', 'tr', 'tk', 'ak', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu', 'yua'] 
#         if language_code not in supported_languages:
#             raise TranslationError(f"Unsupported language: {language_code}")
#         return True

#     def detect_language(self, text):
#         """Detect the language of the input text."""
#         try:
#             detection = self.translator.detect(text)
#             confidence = detection.confidence if detection.confidence is not None else 0.0
#             return detection.lang, confidence
#         except Exception as e:
#             raise TranslationError(f"Language detection failed: {str(e)}")

#     @cache_translation
#     def translate(self, text, dest_language, src_language='auto', max_retries=3):
#         """
#         Translate text to the target language.
#         :param text: Input text to translate.
#         :param dest_language: Target language code (e.g., 'es' for Spanish).
#         :param src_language: Source language code (default: 'auto' for auto-detection).
#         :param max_retries: Maximum number of retries for failed translations.
#         :return: Translated text and confidence score.
#         """
#         self.validate_language(dest_language)
#         chunks = split_text_into_chunks(text)
#         translated_chunks = []

#         for chunk in chunks:
#             for attempt in range(max_retries):
#                 try:
#                     translated = self.translator.translate(chunk, dest=dest_language, src=src_language)
#                     translated_chunks.append(translated.text)
#                     break  # Exit retry loop if translation succeeds
#                 except Exception as e:
#                     if attempt == max_retries - 1:
#                         raise TranslationError(f"Translation failed after {max_retries} retries: {str(e)}")

#         return " ".join(translated_chunks), 1.0  # Confidence score is always 1.0 for now

#     async def translate_async(self, text, dest_language, src_language='auto', max_retries=3):
#         """Asynchronously translate text to the target language."""
#         return await asyncio.get_event_loop().run_in_executor(
#             None, self.translate, text, dest_language, src_language, max_retries
#         )

#     def translate_batch(self, texts, dest_language, src_language='auto', max_retries=3):
#         """
#         Translate a batch of texts to the target language.
#         :param texts: List of input texts to translate.
#         :param dest_language: Target language code.
#         :param src_language: Source language code (default: 'auto').
#         :param max_retries: Maximum number of retries for failed translations.
#         :return: List of translated texts and confidence scores.
#         """
#         return [self.translate(text, dest_language, src_language, max_retries) for text in texts]