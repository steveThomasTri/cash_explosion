from PIL import Image
import pytesseract

import pyautogui

# Set the path to the tesseract executable
# Make sure this path points to where Tesseract is installed on your system

# For Linux/macOS, it might be: "/usr/local/bin/tesseract"

def extractor():
    pytesseract.pytesseract.tesseract_cmd = r'H:\Program Files\Tesseract-OCR\tesseract.exe'  # For Windows users
    screenshot = pyautogui.screenshot(region=(233, 358, 359, 126))
    text = pytesseract.image_to_string(screenshot)
    #print("Extracted Text:", text)
    screenshot2 = pyautogui.screenshot(region=(233, 484, 335, 40))
    text2 = pytesseract.image_to_string(screenshot2)
    #print("Extracted Text:", text2)
    screenshot3 = pyautogui.screenshot(region=(233, 620, 417, 200))
    text3 = pytesseract.image_to_string(screenshot3)
    #print("Extracted Text:", text3)
    return text, text2, text3
# Use pytesseract to do OCR on the image
#text = pytesseract.image_to_string(img)
