import os
import easyocr
import magic
from PIL import Image
from io import BytesIO
from OctoLingo.exceptions import OCRProcessingError
from typing import Union, List, Tuple
import docx
import pdfplumber

class OctoOCR:
    def __init__(self, languages: List[str] = ['en']):
        """
        Initialize the OCR reader with specified languages.
        
        Args:
            languages (List[str]): List of language codes to support for OCR.
                                  Default is ['en'] (English).
        """
        self.reader = easyocr.Reader(languages)
        self.mime = magic.Magic(mime=True)
    
    def _is_image_file(self, file_path: str) -> bool:
        """Check if the file is an image based on MIME type."""
        mime_type = self.mime.from_file(file_path)
        return mime_type.startswith('image/')
    
    def _is_pdf_file(self, file_path: str) -> bool:
        """Check if the file is a PDF."""
        mime_type = self.mime.from_file(file_path)
        return mime_type == 'application/pdf'
    
    def _is_word_file(self, file_path: str) -> bool:
        """Check if the file is a Word document."""
        mime_type = self.mime.from_file(file_path)
        return mime_type in [
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
    
    def _extract_from_image(self, file_path: str) -> str:
        """Extract text from image file."""
        try:
            result = self.reader.readtext(file_path, detail=0)
            return "\n".join(result)
        except Exception as e:
            raise OCRProcessingError(f"Failed to extract text from image: {str(e)}")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            text = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text.append(page.extract_text())
            return "\n".join(text)
        except Exception as e:
            raise OCRProcessingError(f"Failed to extract text from PDF: {str(e)}")
    
    def _extract_from_word(self, file_path: str) -> str:
        """Extract text from Word document."""
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise OCRProcessingError(f"Failed to extract text from Word document: {str(e)}")
    
    def extract_text(self, file_path: str) -> Tuple[str, str]:
        """
        Extract text from a file (image, PDF, or Word document).
        
        Args:
            file_path (str): Path to the file to extract text from.
            
        Returns:
            Tuple[str, str]: Extracted text and detected file type.
            
        Raises:
            OCRProcessingError: If text extraction fails.
            ValueError: If file type is not supported.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if self._is_image_file(file_path):
            return self._extract_from_image(file_path), "image"
        elif self._is_pdf_file(file_path):
            return self._extract_from_pdf(file_path), "pdf"
        elif self._is_word_file(file_path):
            return self._extract_from_word(file_path), "word"
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
    
    def extract_text_from_bytes(self, file_bytes: bytes, file_type: str) -> str:
        """
        Extract text from file bytes.
        
        Args:
            file_bytes (bytes): File content as bytes.
            file_type (str): Type of file ('image', 'pdf', or 'word').
            
        Returns:
            str: Extracted text.
            
        Raises:
            OCRProcessingError: If text extraction fails.
            ValueError: If file type is not supported.
        """
        try:
            if file_type == 'image':
                # Create a temporary image file in memory
                image = Image.open(BytesIO(file_bytes))
                # Save to temporary file (EasyOCR requires file path)
                temp_path = "temp_octoling_ocr_image.png"
                image.save(temp_path)
                try:
                    return self._extract_from_image(temp_path)
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            elif file_type == 'pdf':
                # Save to temporary file
                temp_path = "temp_octoling_ocr.pdf"
                with open(temp_path, 'wb') as f:
                    f.write(file_bytes)
                try:
                    return self._extract_from_pdf(temp_path)
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            elif file_type == 'word':
                # Save to temporary file
                temp_path = "temp_octoling_ocr.docx"
                with open(temp_path, 'wb') as f:
                    f.write(file_bytes)
                try:
                    return self._extract_from_word(temp_path)
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            raise OCRProcessingError(f"Failed to extract text from bytes: {str(e)}")