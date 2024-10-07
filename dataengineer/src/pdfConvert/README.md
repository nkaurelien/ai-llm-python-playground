
# HOW IT WORK

Vous pouvez utiliser abiword ou Apose ou libreoffice

Nous recommendons abiword

# Install


Install Abiword 
```console
sudo apt install abiword
```

or Install libreoffice
```console
sudo add-apt-repository ppa:libreoffice/ppa -y  && \
                                sudo apt update && \
                                sudo apt install libreoffice -y && \
                                sudo apt auto-remove -y && \
                                sudo add-apt-repository --remove ppa:libreoffice/ppa -y
```

or Install Apose-Word

```console
sudo apt-get update  && \
  sudo apt-get install -y dotnet-sdk-7.0 && \
  sudo apt-get install -y aspnetcore-runtime-7.0
  
pip install aspose-words
```

# RUN
```console
/bin/python3 src/pdf2html/useAbiword.py 
```