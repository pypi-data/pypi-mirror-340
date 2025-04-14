import easyocr
import os
from PIL import Image
import io
from OctoLingo.file_handler import FileHandler
from OctoLingo.exceptions import TranslationError
import numpy as np
import re

class OctoOCR:
    def __init__(self, languages=['en'], gpu=False):
        """
        Initialize the EasyOCR reader.
        
        :param languages: List of languages to recognize (default: ['en'])
        :param gpu: Whether to use GPU (default: False)
        """
        try:
            self.reader = easyocr.Reader(languages, gpu=gpu, quantize=False, model_storage_directory='easyocr_models')
        except Exception as e:
            raise TranslationError(f"Failed to initialize OCR: {str(e)}. Make sure EasyOCR is installed.")
        
    def extract_text(self, input_file):
        """
        Extract text from an image file or PDF.
        
        :param input_file: Path to the file or file-like object
        :return: Extracted text
        """
        try:
            if isinstance(input_file, (str, os.PathLike)):
                if not os.path.exists(input_file):
                    raise TranslationError(f"File not found: {input_file}")
                
                ext = os.path.splitext(input_file)[1].lower()
                if ext in ('.pdf'):
                    return self._extract_from_pdf(input_file)
                elif ext in ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'):
                    return self._extract_from_image(input_file)
                else:
                    # Try reading as text file first
                    try:
                        return FileHandler.read_file(input_file)
                    except:
                        raise TranslationError(f"Unsupported file format: {ext}")
            else:
                return self._extract_from_file_object(input_file)
                
        except Exception as e:
            raise TranslationError(f"OCR extraction failed: {str(e)}")

    def _clean_ocr_text(self, text):
        """Clean OCR output thoroughly"""
        # Remove common OCR artifacts
        text = re.sub(r'[^\w\s\-\.\,\'\"]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _extract_from_image(self, image_path):
        """Process image with better text cleaning"""
        try:
            # Preprocess image
            img = Image.open(image_path)
            if img.mode != 'L':
                img = img.convert('L')  # Convert to grayscale
            
            img_array = np.array(img)
            result = self.reader.readtext(
                img_array,
                detail=0,
                paragraph=True,
                contrast_ths=0.5,
                adjust_contrast=0.7
            )
            
            text = ' '.join(result)
            return self._clean_ocr_text(text)
        except Exception as e:
            raise TranslationError(f"Image processing failed: {str(e)}")

    def _extract_from_pdf(self, pdf_path):
        """Extract text from a PDF file."""
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path)
            text = ""
            for img in images:
                result = self.reader.readtext(img, detail=0)
                text += " ".join(result) + "\n"
            return text
        except ImportError:
            raise TranslationError("PDF processing requires pdf2image package. Install with: pip install pdf2image")
        except Exception as e:
            raise TranslationError(f"PDF processing failed: {str(e)}")

    def _extract_from_file_object(self, file_obj):
        """Extract text from a file-like object."""
        try:
            file_content = file_obj.read()
            
            # Try to process as image
            try:
                # Convert to numpy array via PIL
                img = Image.open(io.BytesIO(file_content))
                img_array = np.array(img)
                result = self.reader.readtext(img_array, detail=0)
                return " ".join(result)
            except Exception as img_error:
                # If not an image, try to decode as text
                try:
                    return file_content.decode('utf-8')
                except UnicodeDecodeError:
                    raise TranslationError("File format not supported for OCR")
        except Exception as e:
            raise TranslationError(f"File object processing failed: {str(e)}")