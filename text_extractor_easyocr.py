import easyocr
from PIL import Image
import numpy as np
import os
from datetime import datetime

class OCRProcessor:
    def __init__(self, languages=["en"], log_dir='log', log_file='ocr_results.log'):
        """
        Initialize the OCR processor with the specified languages.

        :param languages: List of languages for OCR
        """
        self.reader = easyocr.Reader(languages)
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)
        self._ensure_log_dir_exists()

    def _ensure_log_dir_exists(self):
        """
        Ensure that the log directory exists. If not, create it.

        :return: None
        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

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
            self.save_to_log(image_path, text)
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
            self.save_to_log("PIL image", text)
            return text
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def save_to_log(self, source, text):
        """
        Save the extracted text along with the source image path to the log file.
        """
        try:
            with open(self.log_file, "a", encoding='utf-8') as log_file:
                log_file.write(f"Source: {source}\n")
                log_file.write(f"Date/Time: {datetime.now()}\n")
                log_file.write(f"Text:\n{text}\n\n")
                log_file.write(f"{'-'*50}\n")
            print(f"Text saved to log file: {self.log_file}")
        except Exception as e:
            print(f"Error saving to log file: {e}")


# Example usage
if __name__ == "__main__":
    # Initialize OCR processor
    ocr_processor = OCRProcessor(languages=["en", "id"])

    # Process an image from file
    image_path = "captured_screen.png"
    extracted_text = ocr_processor.process_image(image_path)
    print(f"Extracted Text from file: {extracted_text}")

    # Process a PIL Image object
    image = Image.open(image_path)
    extracted_text_pil = ocr_processor.process_image_from_pil(image)
    print(f"Extracted Text from PIL Image object: {extracted_text_pil}")
