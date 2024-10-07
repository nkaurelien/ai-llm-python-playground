import os
from jinja2 import Environment, FileSystemLoader
import subprocess
import base64
from faq_parser import parse_faq
from PyPDF2 import PdfFileReader, PdfFileWriter

def combine_pdfs(input_folder_path, output_folder_path, output_filename):
    pdf_writer = PdfFileWriter()
    
    for filename in os.listdir(input_folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_folder_path, filename)
            pdf_reader = PdfFileReader(pdf_path)
            
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)
    
    output_filepath = os.path.join(output_folder_path, output_filename)
    
    # Créer le répertoire de sortie s'il n'existe pas
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    with open(output_filepath, 'wb') as out_pdf_file:
        pdf_writer.write(out_pdf_file)
        

def convert_folder_pdf_to_html(input_folder, output_folder):

    template_path = './resources/views'

    # Template HTML à utiliser
    template_html = 'template.html'

    # Charger le template HTML avec Jinja2
    env = Environment(loader=FileSystemLoader(searchpath=template_path))
    template = env.get_template(template_html)

    # Liste pour stocker les noms des fichiers PDF pour le menu
    menu_items = []

    # Vérifier si AbiWord est installé
    try:
        subprocess.run(["abiword", "--version"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("AbiWord n'est pas installé ou n'est pas accessible. Assurez-vous de l'installer correctement.")
        return

    # Vérifier si les dossiers d'entrée et de sortie existent
    if not os.path.exists(input_folder):
        print(f"Le dossier d'entrée '{input_folder}' n'existe pas.")
        return

    if not os.path.exists(output_folder):
        print(
            f"Le dossier de sortie '{output_folder}' n'existe pas. Création du dossier...")
        os.makedirs(output_folder)

    # Liste des fichiers PDF dans le dossier d'entrée
    pdf_files = [f for f in os.listdir(
        input_folder) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"Aucun fichier PDF trouvé dans le dossier '{input_folder}'.")
        return

    # Convertir chaque fichier PDF en HTML
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        html_file = os.path.splitext(pdf_file)[0] + ".html"
        txt_file = os.path.splitext(pdf_file)[0] + ".txt"
        json_file = os.path.splitext(pdf_file)[0] + ".json"
        html_path = os.path.join(output_folder, html_file)
        json_path = os.path.join(output_folder, json_file)
        txt_path = os.path.join(output_folder, txt_file)

        print(f"Traiement de '{pdf_path}'")

        # Utilisation de abiword pour convertir le fichier PDF en HTML
        try:
            print(f"Generation du HTML")
            subprocess.run(["abiword", "--to=html", pdf_path,
                           "--to-name=" + html_path], check=True)

            print(f"Generation du TXT")
            subprocess.run(["abiword", "--to=txt", pdf_path,
                           "--to-name=" + txt_path], check=True)

            # Ajouter l'élément de menu
            nom_fichier_html = f'{os.path.splitext(pdf_file)[0]}.html'
            nom_fichier_html_sans_faq = nom_fichier_html.replace(
                "• ", "", 1).replace("FAQ", "", 1)
            menu_items.append(
                (nom_fichier_html, os.path.splitext(pdf_file)[0]))

            # Encoder les images en base64 dans le fichier HTML
            # encode_images_to_base64(html_path)

            # Convertir en Json sous forme de Question Response
            print(f"Generation du JSON QA")
            json_key = os.path.splitext(pdf_file)[0].replace("• ", "", 1)
            parse_faq(txt_path, json_key=json_key, output_file=json_path)

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la conversion de '{pdf_path}': {e}")

    # Créer un fichier index.html avec des liens vers tous les fichiers HTML
    index_template = env.get_template('index_template.html')
    index_html_content = index_template.render(menu_items=sorted(menu_items))
    with open(os.path.join(output_folder, 'index.html'), 'w') as f:
        f.write(index_html_content)
    print("Fichier index.html généré avec succès.")


def encode_images_to_base64(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Recherche des balises d'image dans le fichier HTML
    start_tag = '<img src="data:image/'
    end_tag = '"/>'
    img_start_index = html_content.find(start_tag)

    while img_start_index != -1:
        img_end_index = html_content.find(end_tag, img_start_index + 1)
        if img_end_index == -1:
            break

        # Extraire le chemin de l'image
        img_tag = html_content[img_start_index:img_end_index + len(end_tag)]
        img_path_start = img_tag.find('"') + 1
        img_path_end = img_tag.find('"', img_path_start + 1)
        img_path = img_tag[img_path_start:img_path_end]

        # Charger l'image en tant que base64
        if os.path.isfile(img_path):
            with open(img_path, 'rb') as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                html_content = html_content.replace(
                    img_path, f'data:image/{img_path.split(".")[-1]};base64,{img_base64}', 1)

        img_start_index = html_content.find(start_tag, img_start_index + 1)

    # Écrire le contenu HTML mis à jour
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
        print(f"Encodage des images en base64 réussie !")


if __name__ == "__main__":

    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, 'resources/pdf')
    output_path = os.path.join(cwd, 'public_html')
    output_filename = 'FAQ Silae combiné.pdf'
    # convert_folder_pdf_to_html(input_folder_path, output_path)
    combine_pdfs(input_folder_path, output_path, output_filename)
