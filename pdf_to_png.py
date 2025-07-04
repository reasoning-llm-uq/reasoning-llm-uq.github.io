'''
Read files from images folder, if they are pdf files, convert them to png files.
'''
import os
from pdf2image import convert_from_path

# Set your target folder here
FOLDER_PATH = "static/images/"

def convert_pdf_to_png(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.dirname(pdf_path)

        for i, img in enumerate(images):
            img_path = os.path.join(output_dir, f"{base_name}_page_{i+1}.png")
            img.save(img_path, 'png')

        os.remove(pdf_path)
        print(f"Converted and removed: {pdf_path}")

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

def process_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                convert_pdf_to_png(pdf_path)

if __name__ == "__main__":
    process_folder(FOLDER_PATH)
