# securityonion-mcp
This server is a pure mcp-server written in python based on the STANDARD mcp server library. 

## Install Instructions
Ensure python-pip for python3 is installed locally.

```bash
./install.sh
```

## Env for prod
Create a file named .env with the following code:
```bash 
ELASTICSEARCH_HOST=https://localhost:9200
ELASTICSEARCH_USERNAME=<elasticsearch-username>
ELASTICSEARCH_PASSWORD=<elasticsearch-password>
```

## Developer Notes 
Create your virtual py enviornment
```bash
sudo apt install python3.12-venv
python3 -m venv ~/.venv/so-mcp
source ~/.venv/so-mcp/bin/activate
```