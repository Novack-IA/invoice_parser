import os 
import pdfplumber
import pytesseract 
from PIL import Image 
import fitz 

def extract_text_from_pdf(pdf_path):
       text = ""
       with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"

        if len(text.strip()) < 20:
            return extract_text_with_ocr(pdf_path)
        else:
            return text.strip()

def extract_text_with_ocr(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        pix = pdf_document[page_num].get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        text += pytesseract.image_to_string(img , lang = "por") + "\n"
    return text.strip()

def process_all_pdfs(input_folder,output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            text = extract_text_from_pdf(pdf_path)

            output_path = os.path.join(output_folder, filename.replace(".pdf", ".txt"))
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Text extracted and saved to {output_path}")

if __name__ == "__main__":
    input_folder = "data/raw/invoices"
    output_folder = "data/raw/extracted_text"
    process_all_pdfs(input_folder, output_folder)
