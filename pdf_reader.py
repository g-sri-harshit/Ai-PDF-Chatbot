import fitz 
import os 
import io 
import hashlib
from typing import List, Dict
from PIL import Image 
import pytesseract


IMAGE_OUTPUT_DIR = "extracted_images"
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok = True)

def get_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def clean_text(text: str) -> str:
    return " ".join(text.split())

def extract_text_blocks(page) -> List[str]:
    text = page.get_text("text")
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line = clean_text(line)
        if len(line) > 30:
            cleaned.append(line)
    return cleaned

def convert_table_to_sentences(table) -> List[str]:
    structured_rows = []

    try:
        data = table.extract()
        if not data or len(data) < 2:
            return []
        
        headers = data[0]
        for row in data[1]:
            if not any(row):
                continue
            row_text = []

            for header, value in zip(headers, row):
                if header and value:
                    row_text.append(f"{header.strip()}: {str(value).strip()}")

            if row_text:
                structured_rows.append(", ".join(row_text))

    except Exception as e:
        print(f"[Warning] Table error: {e}")

    return structured_rows

def extract_tables(page) -> List[str]:
    table_data = []

    try:
        tables = page.find_tables()

        for table in tables:
            rows = convert_table_to_sentences(table)
            table_data.extend(rows)

    except Exception as e:
        print(f"[Warning] Table extraction error: {e}")

    return table_data


def extract_images_and_ocr(doc, page, page_number) -> List[str]:
    image_texts = []

    try:
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{IMAGE_OUTPUT_DIR}/page_{page_number}_img_{img_index}.{image_ext}"

            with open(image_filename, "wb") as f:
                f.write(image_bytes)

            try:
                image = Image.open(io.BytesIO(image_bytes))
                ocr_text = pytesseract.image_to_string(image)
                ocr_text = clean_text(ocr_text)

                if ocr_text:
                    image_texts.append(ocr_text)

            except Exception as e:
                print(f"[Warning] OCR failed: {e}")

    except Exception as e:
        print(f"[Warning] Image extraction failed: {e}")

    return image_texts

def extract_pdf_content(pdf_path: str) -> List[Dict]:
    doc = fitz.open(pdf_path)

    final_output= []
    seen_hashes = set()
    
    for page_number, page in enumerate(doc, start = 1):
        
        text_blocks = extract_text_blocks(page)
        for text in text_blocks:
            key = get_hash(text)

            if key not in seen_hashes:
                final_output.append({
                    "page" : page_number,
                    "type" : "text",
                    "content" : text
                })
                seen_hashes.add(key)

        tables = extract_tables(page)
        for row in tables:
            key = get_hash(row)

            if key not in seen_hashes:
                final_output.append({
                    "page" : page_number,
                    "type" : "table",
                    "content" : row
                })
                seen_hashes.add(key)


        image_texts = extract_images_and_ocr(doc, page, page_number)

        for text in image_texts:
            key = get_hash(text)

            if key not in seen_hashes:
                final_output.append({
                    "page" : page_number,
                    "type" : "image_ocr",
                    "content" : text
                })
                seen_hashes.add(key)

    return final_output


            









