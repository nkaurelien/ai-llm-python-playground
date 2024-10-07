import os
import subprocess
# from markdownify import markdownify as md
from markdownify import MarkdownConverter
from bs4 import BeautifulSoup  # Importer BeautifulSoup

class CustomMarkdownConverter(MarkdownConverter):


    """
    Create a custom MarkdownConverter that add bold style on a paragraph
    """
    def convert_p(self, el, text, convert_as_inline):
        # textP = text.strip()
        textP = text
        if str(el) == "<p></p>" :
            textP = '\n'
        else:
            style_attr = el.get('style')
            textP = super().convert_b(el, textP, convert_as_inline) if len(textP) and 'font-weight:bold' in str(style_attr) else textP
            textP = super().convert_p( el, textP, convert_as_inline) if len(textP) != 0 else ''
            
            # Transformation des ligne article en titre de niveau 4
            textP = '\n\n#### ' + textP if str(text).lower().startswith('article') and len(text) <= 15 else textP


        return  textP
    
    """
    Create a custom MarkdownConverter that adds two newlines before an heading
    """
    def convert_hn(self, n, el, text, convert_as_inline):
        return'\n\n' + super().convert_hn( n, el, text, convert_as_inline) if text else ''
    
    """
    Create a custom MarkdownConverter that adds two newlines after an image
    """
    def convert_img(self, el, text, convert_as_inline):
        return super().convert_img(el, text, convert_as_inline) + '\n\n' if text else ''

# Create shorthand method for conversion
def md(html, **options):
    return CustomMarkdownConverter(**options).convert(html)


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
            with open(html_path, 'r', encoding='utf-8') as input_file:
                    html_content = input_file.read()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    body_content = soup.find('body')  # Trouver le contenu du body

                    if body_content:
                        markdown_content = md(str(body_content), heading_style='ATX')  # Convertir le contenu du body en Markdown
                    else:
                        markdown_content = md(html_content, heading_style='ATX')  # Fallback si pas de body

                    with open(md_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(markdown_content)
            
            print(f"Conversion réussie !")

        
        except Exception as e:
            print(f"Erreur lors de la conversion de '{html_path}': {e}")
        

if __name__ == "__main__":

    cwd = os.getcwd()
    # input_folder_path = '/home/smartdatapay/Workspaces/Smartdatapay/syntheses'
    input_folder_path = '/home/smartdatapay/Workspaces/Smartdatapay/smartdatapay-distribuable/ccn/dist/html'
    # input_folder_path = os.path.join(cwd, 'storage/data')
    output_folder_path = os.path.join(cwd, 'storage/out')
    convert_folder_html_to_md(input_folder_path, output_folder_path)
