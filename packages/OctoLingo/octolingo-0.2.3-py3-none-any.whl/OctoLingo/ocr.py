import easyocr
import os
from PIL import Image
import io
import numpy as np
import re
from OctoLingo.file_handler import FileHandler
from OctoLingo.exceptions import TranslationError

class OctoOCR:
    def __init__(self, languages=['en'], gpu=False):
        """
        Initialize OCR with strict text validation.
        """
        try:
            self.reader = easyocr.Reader(
                languages,
                gpu=gpu,
                quantize=False,
                model_storage_directory='easyocr_models',
                download_enabled=True
            )
        except Exception as e:
            raise TranslationError(f"OCR initialization failed: {str(e)}")

    def _validate_text(self, text):
        """Ensure text is valid and not binary"""
        if not isinstance(text, str):
            raise TranslationError("OCR returned non-text data")
            
        # Check for binary patterns
        if any(ord(char) > 127 for char in text[:100]):
            raise TranslationError("OCR returned binary-like data")
            
        return True

    def extract_text(self, input_file):
        """
        Extract text with strict validation.
        """
        try:
            if isinstance(input_file, (str, os.PathLike)):
                if not os.path.exists(input_file):
                    raise TranslationError(f"File not found: {input_file}")
                
                ext = os.path.splitext(input_file)[1].lower()
                if ext == '.pdf':
                    text = self._extract_from_pdf(input_file)
                elif ext in {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'}:
                    text = self._extract_from_image(input_file)
                else:
                    try:
                        text = FileHandler.read_file(input_file)
                    except:
                        raise TranslationError(f"Unsupported file format: {ext}")
            else:
                text = self._extract_from_file_object(input_file)
                
            self._validate_text(text)
            return self._clean_text(text)
        except Exception as e:
            raise TranslationError(f"OCR extraction failed: {str(e)}")

    def _clean_text(self, text):
        """Thoroughly clean OCR output"""
        text = re.sub(r'[^\w\s\-\.\,\'\"]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _extract_from_image(self, image_path):
        """Process image with validation"""
        try:
            img = Image.open(image_path)
            if img.mode != 'L':
                img = img.convert('L')
            
            img_array = np.array(img)
            result = self.reader.readtext(
                img_array,
                detail=0,
                paragraph=True,
                contrast_ths=0.5,
                adjust_contrast=0.7
            )
            
            return ' '.join(result)
        except Exception as e:
            raise TranslationError(f"Image processing failed: {str(e)}")

    def _extract_from_pdf(self, pdf_path):
        """Process PDF with validation"""
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path)
            text_parts = []
            
            for img in images:
                try:
                    img = img.convert('L')
                    img_array = np.array(img)
                    result = self.reader.readtext(
                        img_array,
                        detail=0,
                        paragraph=True
                    )
                    text_parts.append(' '.join(result))
                except Exception as e:
                    continue
                    
            return '\n\n'.join(text_parts)
        except ImportError:
            raise TranslationError("PDF processing requires pdf2image")
        except Exception as e:
            raise TranslationError(f"PDF processing failed: {str(e)}")

    def _extract_from_file_object(self, file_obj):
        """Process file object with validation"""
        try:
            file_content = file_obj.read()
            
            try:
                img = Image.open(io.BytesIO(file_content))
                img = img.convert('L')
                img_array = np.array(img)
                result = self.reader.readtext(
                    img_array,
                    detail=0,
                    paragraph=True
                )
                return ' '.join(result)
            except:
                try:
                    return file_content.decode('utf-8')
                except UnicodeDecodeError:
                    raise TranslationError("Unsupported file format")
        except Exception as e:
            raise TranslationError(f"File processing failed: {str(e)}")