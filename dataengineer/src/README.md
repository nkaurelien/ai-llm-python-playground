
# INSTALL


Install python virtual env

```console
pip install --upgrade pip
sudo apt install python3-virtualenv
pip install --upgrade virtualenv
virtualenv -p python3 venv
chmod +x venv/bin/activate
```

Install python lib

```console
pip install -r src/requirements.txt
```

# RUN


Activate python venv
```console
source ./venv/bin/activate
```

```console
python src/pdfConvert/useAbiword.py 
```

## generate website a partir des PDF disponibles

```console
python src/website/app.py 
```

Envoyer par ftp sur le serveur
```console
python src/website/ftp.py 
```