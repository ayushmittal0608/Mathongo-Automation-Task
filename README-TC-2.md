# Image Processing and Optical Character Recognition(OCR)
This Python script processes an image containing a multiple-choice question (MCQ) along with a diagram. It intelligently separates the question text from the diagram and generates two individual image files:
- question.png – containing only the question and options.
- diagram.png – containing only the diagram.

# Tech Stack Used
- Python – core scripting language
- Pytesseract – for OCR (optical character recognition)
- OpenCV (cv2) – for image processing and contour detection
- PIL (Python Imaging Library) – for image handling
- re (regex) – for pattern matching in text

# Features
- Automatically detects and separates textual and visual content
- Outputs clean, cropped image files
- Uses Tesseract OCR and OpenCV for layout understanding

# Installations
- Download the github version of tesseract (well-maintained and highly recommended for Windows).
    Link-https://github.com/tesseract-ocr/tesseract
[Note: Add directory either to environment variables or save it to the program files of C:// Drive.]
- Install pytesseract, cv2, re, and PIL in the terminal.
    pip install  pytesseract cv2 re pil

# File Structure
sample-task-image-processing/
│
├── image-detection.py             # Python script
├── question.png                   # Question file
├── input_image.png                # Input Image file
└── diagram.png                    # Diagram file

# How to Run
1. Open the folder 'sample-task' and navigate to new terminal.
2. Navigate to the directory 'sample-task-image-processing'.
    cd sample-task-image-processing
3. Run the following code in the terminal:
    python image-detection.png