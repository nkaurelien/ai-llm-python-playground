import os
import subprocess
import aspose.words as asposewords

def convert_folder_html_to_md(input_folder, output_folder):
    # Vérifier si les dossiers d'entrée et de sortie existent
    if not os.path.exists(input_folder):
        print(f"Le dossier d'entrée '{input_folder}' n'existe pas.")
        return
    
    if not os.path.exists(output_folder):
        print(f"Le dossier de sortie '{output_folder}' n'existe pas. Création du dossier...")
        os.makedirs(output_folder)

    # Liste des fichiers html dans le dossier d'entrée
    html_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.html')]

    if not html_files:
        print(f"Aucun fichier html trouvé dans le dossier '{input_folder}'.")
        return

    # Convertir chaque fichier html en md
    for html_file in html_files:
        html_path = os.path.join(input_folder, html_file)
        md_file = os.path.splitext(html_file)[0] + ".md"
        md_path = os.path.join(output_folder, md_file)

        print(f"Conversion de '{html_path}' en '{md_path}'...")

        # Utilisation de html2mdEX pour convertir le fichier html en md
        try:
            doc = asposewords.Document(html_path)
            # doc.save(md_path, asposewords.SaveFormat.md)
            doc.save(md_path)
            print(f"Conversion réussie !")

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la conversion de '{html_path}': {e}")

        except Exception as e:
            print(f"Erreur lors de la conversion de '{html_path}': {e}")
        

if __name__ == "__main__":

    cwd = os.getcwd()
    input_folder_path = '/home/smartdatapay/Workspaces/Smartdatapay/syntheses'
    # input_folder_path = '/home/smartdatapay/Workspaces/Smartdatapay/smartdatapay-distribuable/ccn/dist/html'
    # input_folder_path = os.path.join(cwd, 'storage/data')
    output_folder_path = os.path.join(cwd, 'storage/md')
    convert_folder_html_to_md(input_folder_path, output_folder_path)
