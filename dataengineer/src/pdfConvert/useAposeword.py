import os
import subprocess
import aspose.words as asposewords

def convert_folder_pdf_to_html(input_folder, output_folder):
    # Vérifier si les dossiers d'entrée et de sortie existent
    if not os.path.exists(input_folder):
        print(f"Le dossier d'entrée '{input_folder}' n'existe pas.")
        return
    
    if not os.path.exists(output_folder):
        print(f"Le dossier de sortie '{output_folder}' n'existe pas. Création du dossier...")
        os.makedirs(output_folder)

    # Liste des fichiers PDF dans le dossier d'entrée
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"Aucun fichier PDF trouvé dans le dossier '{input_folder}'.")
        return

    # Convertir chaque fichier PDF en HTML
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        html_file = os.path.splitext(pdf_file)[0] + ".html"
        html_path = os.path.join(output_folder, html_file)

        print(f"Conversion de '{pdf_path}' en '{html_path}'...")

        # Utilisation de pdf2htmlEX pour convertir le fichier PDF en HTML
        try:
            doc = asposewords.Document(pdf_path)
            doc.save(html_path, asposewords.SaveFormat.HTML)
            print(f"Conversion réussie !")

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la conversion de '{pdf_path}': {e}")
        except FileNotFoundError:
            print("pdf2htmlEX n'est pas installé ou n'est pas accessible. Assurez-vous de l'installer correctement.")
            return

if __name__ == "__main__":

    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, 'storage/data')
    output_folder_path = os.path.join(cwd, 'storage/out')
    convert_folder_pdf_to_html(input_folder_path, output_folder_path)


    # for filename in os.listdir(pdf_dir):
    #     if filename.endswith('.pdf'):

    #         pdf = pdfquery.PDFQuery(os.path.join(pdf_dir, filename))
    #         pdf.load()

    #         #convert the pdf to XML
    #         pdf.tree.write(os.path.join(out_dir, filename+'.xml'), pretty_print = True)
    #         pdf
