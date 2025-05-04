# SecurityOnion MCP Server
This mcp-server is designed as a standalone server that can be deployed on Security Onion (v2.3.1+) installations. It provides a flexible foundation for managing MCP communication workflows.

You can extend its functionality by adding subservers to the tools/ directory. With minimal changes, it's easy to build in additional capabilities tailored to your environment.

## 🤝 Contributing & Collaboration
I'm actively developing this project at a steady pace — and I welcome feedback, questions, feature ideas, or contributions of any kind.

This project is released under the Apache 2.0 License.
Corporate developers are especially encouraged to contribute and help improve its utility in operational environments.

## Tool-calls:
1. tools/so_elasticsearch_mcp 
- earch_elasticsearch
- list_indices
2. tools/so_files_mcp
- get_zeek_file
- get_suricata_pcap
- get_strelka_file

## Requirements:
SecurityOnion V2.13+ Host
ElasticSearch == 8
SecurityOnion must have an internet connection, if not, please review the "Installer Fails" section.

## Install Instructions
If internet access is available, the install.sh script will automatically download the official get-pip.py installer, install pip for Python3, install the required Python packages from requirements.txt, and create a local virtual environment.

During setup, the script will prompt you to provide credentials for accessing the Security Onion Elasticsearch database. These values are saved to a .env file in the current directory. The application reads this .env file to obtain the Elasticsearch base URL, username, and password.

Once configured, the server runs and exposes a remote interface on TCP port 5001 to receive and handle incoming requests.

```shell
./install.sh
```

## Configure Securityonion firewall
To allow outbound connections to the mcp-server, we will need to write a rule to allow connections from your remote mcp client.
```shell
sudo so-firewall --help
sudo firewall-cmd --state # check if the firewall is running (if not, then you can skip adding the remote host)

# Get active zones (you may need to change the --zone flag for next set of commands)
sudo firewall-cmd --get-active-zones

# Add port to a zone
sudo firewall-cmd --zone=SecurityOnion --add-port=5001/tcp --permanent
sudo firewall-cmd --reload

```

Note that you can modify the .env and update params:
```shell
nano .env
```

## Running the Server
Run the following bash script:
```shell
./run.sh
```

## How to add other MCP-servers 
You can add other mcp servers by downloading them and placing them into the tools/ directory. Note that these servers will need to use FastMCP (as far as I know). Also note that you will need to makesure they're importable in server.py->setup() function. If you understand python well enough this should be easy.

## Help Guides
# Installer Fails:
This project assumes that your securityonion services has internet! Note that you're not entirely out of luck. I recommend reading about how to 'compile' python software into single package binaries. You can use pyinstaller! 

# .Env for prod 
Create a file named .env with the following code (note install.sh should have done this already):
```bash 
ELASTICSEARCH_HOST=https://localhost:9200
ELASTICSEARCH_USERNAME=<elasticsearch-username>
ELASTICSEARCH_PASSWORD=<elasticsearch-password>
```

# Developer Notes 
Create your virtual py enviornment
```shell
sudo apt install python3.12-venv
python3 -m venv ~/.venv/so-mcp
source ~/.venv/so-mcp/bin/activate
```