import unittest
import os
import io
import asyncio
from PIL import Image, ImageDraw, ImageFont
from OctoLingo.translator import OctoLingo
from OctoLingo.glossary import Glossary
from OctoLingo.ocr import OctoOCR   
from OctoLingo.exceptions import TranslationError

class TestOctoLingoOCR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create test files once before all tests run"""
        cls.create_test_image()
        cls.create_test_text_file()
        
    @classmethod
    def create_test_image(cls):
        """Create a simple test image if it doesn't exist"""
        cls.test_image_path = "test_octoling_image.png"
        if not os.path.exists(cls.test_image_path):
            img = Image.new('RGB', (500, 200), color='white')
            try:
                draw = ImageDraw.Draw(img)
                # Try to load a basic font
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    # Fallback to default font
                    font = ImageFont.load_default()
                draw.text((20, 20), "This is a test image for OctoLingo OCR", fill='black', font=font)
                draw.text((20, 60), "Second line of text for testing", fill='black', font=font)
                draw.text((20, 100), "The quick brown fox jumps over the lazy dog", fill='black', font=font)
                # Add some simple shapes for better OCR testing
                draw.rectangle([(20, 140), (120, 160)], fill='red')
                draw.ellipse([(140, 140), (240, 160)], fill='blue')
                img.save(cls.test_image_path, dpi=(300, 300))
            except Exception as e:
                print(f"Couldn't create proper test image: {str(e)}")
                # Fallback to simple image
                img.save(cls.test_image_path)

    @classmethod
    def create_test_text_file(cls):
        """Create a simple test text file if it doesn't exist"""
        cls.test_text_path = "test_octoling_text.txt"
        if not os.path.exists(cls.test_text_path):
            with open(cls.test_text_path, 'w', encoding='utf-8') as f:
                f.write("This is a test text file for OctoLingo translation\n")
                f.write("Second line of text for testing purposes")

    def setUp(self):
        """Initialize a fresh OctoLingo instance for each test"""
        self.octo = OctoLingo(ocr_languages=['en'])
        self.glossary = Glossary()
        self.glossary.add_term("OctoLingo", "OctoTraductor")
        self.glossary.add_term("test", "prueba")

    def test_ocr_text_extraction(self):
        """Test basic OCR text extraction from image"""
        text = self.octo.ocr.extract_text(self.test_image_path)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
        self.assertIn("test image for OctoLingo OCR", text)
        self.assertIn("Second of text", text)

    def test_translate_file_with_ocr(self):
        """Test end-to-end file translation with OCR"""
        try:
            translated, confidence = self.octo.translate_file(self.test_image_path, 'es')
            self.assertIsInstance(translated, str)
            self.assertGreater(len(translated), 0)
            self.assertEqual(confidence, 1.0)
        except TranslationError as e:
            if "NoneType" in str(e):
                self.skipTest("Google Translate API currently unavailable")
            raise

    def test_translate_text_file(self):
        """Test regular text file translation"""
        translated, confidence = self.octo.translate_file(self.test_text_path, 'fr')
        self.assertIsInstance(translated, str)
        self.assertGreater(len(translated), 0)
        self.assertEqual(confidence, 1.0)

    def test_file_object_processing(self):
        """Test processing file-like objects"""
        with open(self.test_image_path, 'rb') as f:
            text = self.octo.ocr.extract_text(f)
            self.assertIsInstance(text, str)
            self.assertGreater(len(text), 0)

    def test_ocr_error_handling(self):
        """Test error handling for unsupported files"""
        with self.assertRaises(TranslationError):
            self.octo.ocr.extract_text("nonexistent_file.txt")

    def test_multilingual_ocr(self):
        """Test OCR with multiple languages"""
        octo_multi = OctoLingo(ocr_languages=['en', 'es'])
        text = octo_multi.ocr.extract_text(self.test_image_path)
        self.assertIsInstance(text, str)

    def test_async_file_translation(self):
        """Test async file translation"""
        async def run_test():
            return await self.octo.translate_file_async(self.test_text_path, 'de')
        
        translated, confidence = asyncio.run(run_test())
        self.assertIsInstance(translated, str)
        self.assertGreater(len(translated), 0)
        self.assertEqual(confidence, 1.0)

    def test_glossary_integration(self):
        """Test integration with glossary"""
        translated, _ = self.octo.translate_file(self.test_text_path, 'es')
        processed = self.glossary.apply_glossary(translated)
        self.assertIn("prueba", processed.lower())

    def test_batch_processing(self):
        """Test batch processing of multiple files"""
        files = [self.test_image_path, self.test_text_path]
        results = []
        
        for file in files:
            try:
                translated, _ = self.octo.translate_file(file, 'it')
                results.append((file, translated))
            except Exception as e:
                results.append((file, str(e)))
        
        self.assertEqual(len(results), 2)
        for file, result in results:
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)

    def test_pdf_processing(self):
        """Test PDF processing (skipped if no test PDF available)"""
        test_pdf = "test_octoling_doc.pdf"
        if not os.path.exists(test_pdf):
            self.skipTest("Test PDF not available")
            
        text = self.octo.ocr.extract_text(test_pdf)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)

    def test_invalid_language_handling(self):
        """Test handling of invalid language codes"""
        with self.assertRaises(TranslationError):
            self.octo.translate("Test text", 'xxx')

    def test_large_file_handling(self):
        """Test handling of large text chunks"""
        large_text = " ".join(["This is a test sentence."] * 1000)
        translated, _ = self.octo.translate(large_text, 'es')
        self.assertIsInstance(translated, str)
        self.assertGreater(len(translated), 0)

if __name__ == '__main__':
    unittest.main()