# Set the path to the tesseract executable
# Make sure this path points to where Tesseract is installed on your system

import cv2
import numpy as np
import mss
from paddleocr import PaddleOCR

# --- Plug in your coordinates here (from calibrate.py / region.json) ---
X_MIN = 116
Y_MIN = 303
X_MAX = 586
Y_MAX = 791
# ------------------------------------------------------------------

# Initialize once (this is the only slow part — model loading)
ocr = PaddleOCR(
    use_textline_orientation=True,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    lang="en",
    enable_mkldnn=False,  # Works around a PaddlePaddle CPU/oneDNN bug
)


def grab_region():
    with mss.mss() as sct:
        bbox = {
            "left": X_MIN,
            "top": Y_MIN,
            "width": X_MAX - X_MIN,
            "height": Y_MAX - Y_MIN,
        }
        shot = sct.grab(bbox)
        img = np.array(shot)  # BGRA
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def get_lines(img):
    results = ocr.predict(img)
    lines = []
    for res in results:
        data = res.json["res"]
        texts = data.get("rec_texts", [])
        boxes = data.get("rec_boxes", [])
        for text, box in zip(texts, boxes):
            if text:
                top_y = box[1] if len(box) >= 2 else 0
                lines.append((top_y, text))
    lines.sort(key=lambda pair: pair[0])
    return [text for _, text in lines]


def extractor():

    cropped = grab_region()
    lines = get_lines(cropped)

    if not lines:
        print("[No text found in region]")
    else:
        for i, line in enumerate(lines):
            print(f"{i}: {line}")

    text = f"{lines[0]} {lines[1]}"
    text2 = f"{lines[2]}"
    text3 = f"{lines[3]}\n{lines[4]}\n{lines[5]}\n{lines[6]}"
    return text, text2, text3
