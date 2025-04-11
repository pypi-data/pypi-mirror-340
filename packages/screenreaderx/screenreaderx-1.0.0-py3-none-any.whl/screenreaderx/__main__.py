import argparse
import easyocr
import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image

class ScreenReader:
    def __init__(self, lang='eng', engine='easyocr'):
        self.lang = lang
        self.engine = engine.lower()

        if self.engine == 'easyocr':
            self.reader = easyocr.Reader([self.lang], gpu=False)

    def capture_screen(self):
        screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    def read_screen(self):
        img = self.capture_screen()

        if self.engine == 'easyocr':
            results = self.reader.readtext(img)
            return [
                {'text': text, 'box': box}
                for box, text, _ in results
            ]

        elif self.engine == 'tesseract':
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            pil_img = Image.fromarray(gray)
            data = pytesseract.image_to_data(pil_img, lang=self.lang, output_type=pytesseract.Output.DICT)
            results = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 60:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    results.append({'text': data['text'][i], 'box': [(x, y), (x+w, y+h)]})
            return results

    def draw_results(self, results):
        img = self.capture_screen()
        for result in results:
            text, box = result['text'], result['box']
            pt1 = tuple(map(int, box[0]))
            pt2 = tuple(map(int, box[2])) if len(box) > 2 else (pt1[0]+150, pt1[1]+30)
            cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
            cv2.putText(img, text, (pt1[0], pt1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Detected Texts", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description="ScreenReaderX - Advanced Screen OCR")
    parser.add_argument("command", help="Command to run (e.g. readall)")
    parser.add_argument("--lang", default="eng", help="Language code (default: eng)")
    parser.add_argument("--engine", default="easyocr", help="OCR engine: easyocr or tesseract")
    parser.add_argument("--show", action="store_true", help="Show results with boxes")
    args = parser.parse_args()

    if args.command == "readall":
        reader = ScreenReader(lang=args.lang, engine=args.engine)
        results = reader.read_screen()
        for result in results:
            print(f"{result['text']} - {result['box']}")

        if args.show:
            reader.draw_results(results)
    else:
        print("Unknown command.")