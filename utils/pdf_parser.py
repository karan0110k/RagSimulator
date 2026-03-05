import fitz
import os

def extract_text_and_images(path, image_folder="extracted_images"):

    doc = fitz.open(path)
    text = ""
    image_paths = []

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    for page_index in range(len(doc)):
        page = doc[page_index]

        # Extract text
        text += page.get_text()

        # Extract images
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_path = f"{image_folder}/page{page_index+1}_{img_index}.{image_ext}"

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_paths.append(image_path)

    return text, image_paths