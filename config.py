import os
from dotenv import load_dotenv

load_dotenv()

# File directories
ZEEK_DIR = "/nsm/zeek/extracted/complete"
SURICATA_DIR = "/nsm/suripcap/1"
STRELKA_DIR = "/nsm/strelka/processed"

# Elasticsearch server config
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "https://localhost:9200")
ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME", "elastic")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "changeme")
