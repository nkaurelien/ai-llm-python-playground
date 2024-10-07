import os
from jinja2 import Environment, FileSystemLoader
import subprocess
import base64


def rebuild_view_index(input_folder, output_folder):
    
    template_path='./resources/views'

    # Charger le template HTML avec Jinja2
    env = Environment(loader=FileSystemLoader(searchpath=template_path))

    # Liste pour stocker les noms des fichiers PDF pour le menu
    menu_items = []


    # Vérifier si les dossiers d'entrée et de sortie existent
    if not os.path.exists(input_folder):
        print(f"Le dossier d'entrée '{input_folder}' n'existe pas.")
        return

    if not os.path.exists(output_folder):
        print(
            f"Le dossier de sortie '{output_folder}' n'existe pas. Création du dossier...")
        os.makedirs(output_folder)

    # Liste des fichiers HTML dans le dossier d'entrée
    html_files = [f for f in os.listdir(
        input_folder) if f.lower().endswith('.html') and not f.lower().startswith('index') and not f.lower().startswith('404')]

    if not html_files:
        print(f"Aucun fichier HTML trouvé dans le dossier '{input_folder}'.")
        return

    # Convertir chaque fichier PDF en HTML
    for html_file in html_files:
        txt_file = os.path.splitext(html_file)[0] + ".txt"
        html_path = os.path.join(output_folder, html_file)

        print(f"Ajout du menu '{html_path}'")


        # Utilisation de abiword pour convertir le fichier PDF en HTML
        try:
   
            # Ajouter l'élément de menu
            nom_fichier_html = f'{os.path.splitext(html_file)[0]}.html'
            # nom_fichier_html_sans_faq = nom_fichier_html.replace("• FAQ", "", 1)
            menu_items.append((nom_fichier_html, os.path.splitext(html_file)[0]))
            
            # Encoder les images en base64 dans le fichier HTML
            # encode_images_to_base64(html_path)

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'ajout dans le menu '{html_file}': {e}")

    # Créer un fichier index.html avec des liens vers tous les fichiers HTML
    index_template = env.get_template('index_template.html')
    index_html_content = index_template.render(menu_items=sorted(menu_items))
    with open(os.path.join(output_folder, 'index.html'), 'w') as f:
        f.write(index_html_content)
    print("Fichier index.html généré avec succès.")


if __name__ == "__main__":

    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, 'public_html')
    output_path = os.path.join(cwd, 'public_html')
    # convert_folder_pdf_to_website(input_folder_path, output_path)
    rebuild_view_index(input_folder_path, output_path)
