from ftplib import FTP
from dotenv import load_dotenv
import os


load_dotenv()


# Paramètres FTP
ftp_host = os.getenv("FTP_HOST")
ftp_user = os.getenv("FTP_USER")
ftp_password = os.getenv("FTP_PASSWORD")
remote_path = os.getenv("FTP_REMOTE_PATH")

# Répertoire local contenant les fichiers HTML à télécharger
cwd = os.getcwd()
local_path = os.path.join(cwd, 'public_html')

# Connexion au serveur FTP
ftp = FTP(ftp_host)
ftp.login(user=ftp_user, passwd=ftp_password)

# Changement de répertoire sur le serveur FTP
ftp.cwd(remote_path)


# ----------------- FONCTIONS ----------------

# Fonction pour creer un fichier .htaccess

def create_robots_txt():
    robots_txt_content = "User-agent: *\nDisallow: /"

    with open("public_html/robots.txt", "w") as robots_file:
        robots_file.write(robots_txt_content)

    print("robots.txt file created.")


# Fonction pour creer un fichier .htaccess

def create_htaccess():

    content = '''<ifModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !\.(js|css|gif|jpg|jpeg|png|ico|swf|pdf|html|php|json|svg)$
RewriteCond %{REQUEST_URI} !^index
RewriteRule (.*) index.html [L]
</ifModule>'''

    # Création et écriture du fichier .htaccess
    local_htaccess_path = 'public_html/.htaccess'
    with open(local_htaccess_path, 'w') as file:
        file.write(content)

    # Ouverture du fichier en mode lecture binaire et upload vers le serveur FTP
    # with open(local_htaccess_path, 'rb') as file:
    #     ftp.storbinary(f'STOR .htaccess', file)

    print("Le fichier .htaccess a été créé.")

# Fonction pour supprimer un fichier


def delete_file(filename):

    # Suppression du fichier
    try:
        ftp.delete(filename)
        print(f"Le fichier {filename} a été supprimé.")
    except:
        print(
            f"Une erreur est survenue lors de la suppression du fichier {filename}.")

# Fonction pour liste un repertoire

def list_ftp_directory():

    # Liste des fichiers et dossiers
    files = []
    ftp.retrlines('LIST', files.append)

    for file in files:
        print(file)

# Fonction pour télécharger un fichier

def upload_file(local_file_path, remote_file_name):
    with open(local_file_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_file_name}', file)


# ----------------- EXECUTION ----------------

# list_ftp_directory()
create_htaccess()

create_robots_txt()

delete_file('default_index.html')

# Parcourir les fichiers locaux et les télécharger
for filename in os.listdir(local_path):
    local_file_path = os.path.join(local_path, filename)
    upload_file(local_file_path, filename)
    print(f"Fichier {filename} téléchargé avec succès.")

list_ftp_directory()

# Fermeture de la connexion FTP
ftp.quit()

print("Tous les fichiers ont été téléchargés avec succès.")
