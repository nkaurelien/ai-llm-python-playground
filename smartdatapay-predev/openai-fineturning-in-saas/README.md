
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
source ./venv/bin/activate
pip install -r src/requirements.txt
```

Modifier l’environnement des variables

```console
cp -r src/.env.example src/.env

```


# HOW IT WORK



# RUN

Activate python venv
```console
source ./venv/bin/activate
```

## Generer le site web à partir des PDF disponibles

```console
python src/train.py 
```