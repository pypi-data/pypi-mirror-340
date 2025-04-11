from PIL import Image
import pytesseract

class OCRProcessor:
    def extract_text(image_path):
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text