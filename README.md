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

## SecurityOnion Requirements:
- SecurityOnion V2.13+ Host
- ElasticSearch == 8
- SecurityOnion must have an internet connection, if not, please review the "Installer Fails" section.
- Python3.10 must be isntalled

## Dev Install Instructions
If internet access is available, the install.sh script will automatically download the official `get-pip.py` installer, install pip for Python3, install the required Python packages from requirements.txt, and create a local virtual environment.

```shell
sudo dnf install -y oraclelinux-release-el9 dnf-utils
sudo dnf config-manager --enable ol9_codeready_builder
sudo dnf repolist enabled

sudo dnf groupinstall "Development Tools" -y
sudo dnf install gcc openssl-devel bzip2-devel libffi-devel wget make zlib-devel -y

cd /usr/src
sudo wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
sudo tar xzf Python-3.10.14.tgz
cd Python-3.10.14
sudo ./configure --enable-optimizations
sudo make -j$(nproc)
sudo make altinstall

```
Then cd back to where you cloned this repo:
```
cd securityonion-mcp
./install.sh
```
Note that you will be prompted to type in information for the security onion host, username, and password.

## Server config.ini
The python config.py code creates a file under (local user home dir) `~/.so-mcp/config.ini` with the file permission: `0666` (user Read/Write only).

Note, you can also run `python3 config.py` to interactively configure the config.ini and view the variables there.\


## Dev Build Instructions
I couldn't get the build.sh to build a working for securityonion (because they have noexec issues), this is something that I would like to get working in the future.

To get the software repo running on a stand security onion dsitro, you will need to run the following commands (note that modifies dnf and your securityonion intall... beware)


## Configure Securityonion firewall
To allow outbound connections to the mcp-server, we will need to write a rule to allow connections from your remote mcp client.

Easy solution that worked for me (if firewalld is down):
```shell
sudo iptables -I INPUT -p tcp --dport 5001 -j ACCEPT
```

```shell
sudo so-firewall --help
sudo firewall-cmd --state # check if the firewall is running (if not, then you can skip adding the remote host)

# Get active zones (you may need to change the --zone flag for next set of commands)
sudo firewall-cmd --get-active-zones

# Add port to a zone
sudo firewall-cmd --zone=SecurityOnion --add-port=5001/tcp --permanent
sudo firewall-cmd --reload
```

## Running the Server
Run the following bash script:
```shell
./run.sh
```

## How to add other MCP-servers 
You can add other mcp servers by downloading them and placing them into the `tools/` directory. Note that these servers will need to use FastMCP (as far as I know). Also note that you will need to makesure they're importable in `server.py->setup()` function. If you understand python well enough this should be easy.