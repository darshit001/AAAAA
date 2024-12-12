import easyocr
import fitz  # PyMuPDF
import os

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # Open the PDF using PyMuPDF (fitz)
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf.load_page(page_num)
                page_text = page.get_text("text")  # Extract text from the page
                if page_text:
                    text += f"Text Layer (Page {page_num + 1}):\n{page_text}\n\n"
                else:
                    print(f"No text layer found on Page {page_num + 1}.")
    except Exception as e:
        print(f"Text extraction failed: {e}")
    return text

def extract_images_from_pdf(pdf_path):
    text = ""
    try:
        # Open the PDF using PyMuPDF (fitz)
        with fitz.open(pdf_path) as pdf:
            for i in range(pdf.page_count):
                page = pdf.load_page(i)
                # Extract image(s) from the page
                image_list = page.get_images(full=True)

                if image_list:
                    text += f"Image Layer (OCR Text on Page {i + 1}):\n"
                    for img_index, img in enumerate(image_list):
                        xref = img[0]
                        base_image = pdf.extract_image(xref)
                        image_bytes = base_image["image"]

                        # Use EasyOCR to extract text from the image
                        result = reader.readtext(image_bytes)
                        for detection in result:
                            text += f"{detection[1]}\n"
                    text += "\n"
                else:
                    print(f"No images found on Page {i + 1}.")
    except Exception as e:
        print(f"Image-based OCR extraction failed: {e}")
    return text

def extract_text_and_images(pdf_path):
    text = ""
    try:
        # First extract text from the text layer using PyMuPDF
        text += extract_text_from_pdf(pdf_path)

        # Then extract text from images using OCR (EasyOCR)
        text += extract_images_from_pdf(pdf_path)
        
    except Exception as e:
        print(f"Layer extraction failed: {e}")
    return text

# Specify the path to the PDF file directly
pdf_path = input("Please enter the full path to the PDF file: ").strip()

# Check if the file exists
if os.path.isfile(pdf_path):
    # Extract text and images from both layers
    text = extract_text_and_images(pdf_path)

    # Output the extracted text
    if text:
        print("Extracted Text from Both Layers:")
        print(text)
    else:
        print("No text or image-based text found in the PDF.")
else:
    print("The file does not exist. Please check the path and try again.")