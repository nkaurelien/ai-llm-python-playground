import os
import subprocess
import pdf2image
import base64

def convert_folder_pdf_to_word_doc(input_folder, output_folder):

    # Vérifier si AbiWord est installé
    try:
        subprocess.run(["abiword", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("AbiWord n'est pas installé ou n'est pas accessible. Assurez-vous de l'installer correctement.")
        return
    
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
        doc_file = os.path.splitext(pdf_file)[0] + ".docx"
        doc_path = os.path.join(output_folder, doc_file)

        print(f"Conversion de '{pdf_path}' en '{doc_path}'...")

        # Utilisation de abiword pour convertir le fichier PDF en HTML
        try:
            subprocess.run(["abiword", "--to=doc", pdf_path, "--to-name=" + doc_path], check=True)
            print(f"Conversion réussie !")

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la conversion de '{pdf_path}': {e}")

def convert_folder_pdf_to_txt(input_folder, output_folder):

    # Vérifier si AbiWord est installé
    try:
        subprocess.run(["abiword", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("AbiWord n'est pas installé ou n'est pas accessible. Assurez-vous de l'installer correctement.")
        return
    
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

    # Convertir chaque fichier PDF en TXT
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        txt_file = os.path.splitext(pdf_file)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_file)

        print(f"Conversion de '{pdf_path}' en '{txt_path}'...")

        # Utilisation de abiword pour convertir le fichier PDF en TXT
        try:
            subprocess.run(["abiword", "--to=txt", pdf_path, "--to-name=" + txt_path], check=True)
            print(f"Conversion réussie !")


        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la conversion de '{pdf_path}': {e}")

def convert_folder_pdf_to_html(input_folder, output_folder):

    # Vérifier si AbiWord est installé
    try:
        subprocess.run(["abiword", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("AbiWord n'est pas installé ou n'est pas accessible. Assurez-vous de l'installer correctement.")
        return
    
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

        # Utilisation de abiword pour convertir le fichier PDF en HTML
        try:
            subprocess.run(["abiword", "--to=html", pdf_path, "--to-name=" + html_path], check=True)
            print(f"Conversion réussie !")

            # Encoder les images en base64 dans le fichier HTML
            encode_images_to_base64(html_path)

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la conversion de '{pdf_path}': {e}")

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
                html_content = html_content.replace(img_path, f'data:image/{img_path.split(".")[-1]};base64,{img_base64}', 1)
        
        img_start_index = html_content.find(start_tag, img_start_index + 1)

    # Écrire le contenu HTML mis à jour
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
        print(f"Encodage des images en base64 réussie !")


if __name__ == "__main__":

    cwd = os.getcwd()
    input_folder_path = '/home/smartdatapay/Workspaces/Smartdatapay/smartdatapay-distribuable/ccn/dist/pdf'

    # input_folder_path = os.path.join(cwd, 'storage/pdf')
    output_html_path = os.path.join(cwd, 'storage/html')
    output_txt_path = os.path.join(cwd, 'storage/txt')
    output_images_path = os.path.join(cwd, 'storage/images')
    output_docs_path = os.path.join(cwd, 'storage/docs')
    # convert_folder_pdf_to_html(input_folder_path, output_html_path)
    convert_folder_pdf_to_txt(input_folder_path, output_txt_path)
    # convert_folder_pdf_to_word_doc(input_folder_path, output_docs_path)
    # convert_folder_pdf_to_images(input_folder_path, output_images_path)

 