import os
import pdf2image

def convert_folder_pdf_to_images(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                images = pdf2image.convert_from_path(pdf_path)
                pdf_name = os.path.splitext(file)[0]
                for i, image in enumerate(images):
                    image_path = os.path.join(output_folder, f"{pdf_name}_page{i + 1}.png")
                    image.save(image_path)


if __name__ == "__main__":

    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, 'storage/pdf')
    output_images_path = os.path.join(cwd, 'storage/images')
    convert_folder_pdf_to_images(input_folder_path, output_images_path)

 