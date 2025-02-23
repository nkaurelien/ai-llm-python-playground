
# INSTALL
Install python virtual env if not exists

```console
sudo apt install python3-virtualenv
pip install --upgrade virtualenv
virtualenv -p python3 venv
chmod +x venv/bin/activate
```

Install python lib

```console
pip install -r src/requirements.txt
```

Modifier l’environnement des variables

```console
cp -r src/.env.example src/.env

```


# HOW IT WORK

Copier les fichiers PDF à convertir dans le répertoire `resources/pdf`

# RUN

Activate python venv
```console
source ./venv/bin/activate
```

## Generer le site web à partir des PDF disponibles

```console
python src/app.py 
```


## Refaire le menu du template

si vous souhaitez refaire le menu sans vouloir reconvertir les fichiers à nouveau.

```console
python src/menu.py 
```

## upload website

Envoyer les fichiers html générés par FTP sur le serveur
```console
python src/ftp.py 
```

Deployer sur firebase

```console
python src/deploy.py 
```

## Deploy to firebase


0. Prerequis

Installé Node.js (ce qui inclut npm, le gestionnaire de paquets de Node).

Installé Firebase CLI en exécutant la commande `npm install -g firebase-tools`.

Connecté à Firebase en utilisant la commande firebase login.

1. Login

```console
 firebase login

```

2. Push the code

```console
 firebase deploy --only hosting -m "Deploying the best new feature ever."

```