
import pdfquery
import os


import os
import pdf2image

def convert_folder_pdf_to_xml(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, filename)
                pdf = pdfquery.PDFQuery(pdf_path)
                pdf.load()

                #convert the pdf to XML
                pdf.tree.write(os.path.join(output_folder, filename+'.xml'), pretty_print = True)
                pdf



if __name__ == "__main__":

    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, 'storage/pdf')
    output_xml_path = os.path.join(cwd, 'storage/xml')
    convert_folder_pdf_to_xml(input_folder_path, output_xml_path)

 