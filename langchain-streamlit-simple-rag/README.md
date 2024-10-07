
# Install Ollama in docker
https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image

```shell
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main

# docker exec -it ollama ollama pull llama2
docker exec -it ollama ollama pull nomic-embed-text
```