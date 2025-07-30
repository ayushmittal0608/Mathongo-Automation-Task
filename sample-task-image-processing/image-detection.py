import pytesseract
from PIL import Image, ImageDraw, ImageFont
import cv2
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = Image.open('input_image.png')

raw_text = pytesseract.image_to_string(image)
text_no_extra_spaces = re.sub(r'[ \t]+', ' ', raw_text)
cleaned_text = re.sub(r'\n\s*\n', '\n', text_no_extra_spaces)

print("Final Cleaned Text:\n", cleaned_text)

def text_to_png(text, output_path='question.png', img_width=300, bg_color=(255, 255, 255),

    text_color=(0, 0, 0), font_path='times.ttf', font_size=12):
    lines = text.strip().split('\n')
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
    
    bbox = font.getbbox('A')
    line_height = bbox[3] - bbox[1] + 4
    img_height = line_height * len(lines) + 20

    img = Image.new('RGB', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    y_text = 10
    for line in lines:
        draw.text((10, y_text), line.strip(), font=font, fill=text_color)
        y_text += line_height

    img.save(output_path)
    print(f"Text converted to image saved at: {output_path}")
    return output_path

text_img_path = text_to_png(cleaned_text, output_path='question.png')

def extract_question_and_diagram(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    if w * h > 1000:
        diagram_img = img[y:y+h, x:x+w]
        cv2.imwrite("diagram.png", diagram_img)
        print("Saved: diagram.png")
    else:
        print("Largest contour too small.")

extract_question_and_diagram("input_image.png")

