import easyocr
from PIL import Image
import numpy as np


class OCRProcessor:
    def __init__(self, languages=["en"]):
        """
        Initialize the OCR processor with the specified languages.

        :param languages: List of languages for OCR
        """
        self.reader = easyocr.Reader(languages)

    def process_image(self, image_path):
        """
        Process an image from file path and extract text using OCR.

        :param image_path: Path to the image file
        :return: Extracted text
        """
        try:
            # Perform OCR on the image file
            results = self.reader.readtext(image_path)
            text = " ".join([result[1] for result in results])
            return text
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def process_image_from_pil(self, image):
        """
        Process a PIL image object and extract text using OCR.

        :param image: PIL Image object
        :return: Extracted text
        """
        try:
            # Convert PIL image to numpy array
            image_np = np.array(image)
            # Perform OCR on the image
            results = self.reader.readtext(image_np)
            text = " ".join([result[1] for result in results])
            return text
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Initialize OCR processor
    ocr_processor = OCRProcessor(languages=["en", "id"])

    # Process an image from file
    image_path = "captured_screen_EN.png"
    extracted_text = ocr_processor.process_image(image_path)
    print(f"Extracted Text from file: {extracted_text}")

    # Process a PIL Image object
    image = Image.open(image_path)
    extracted_text_pil = ocr_processor.process_image_from_pil(image)
    print(f"Extracted Text from PIL Image object: {extracted_text_pil}")
