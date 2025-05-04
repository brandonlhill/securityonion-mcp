import os
import sys
import configparser
import logging
import stat

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# TODO: add these to the config file reader
# File directories
ZEEK_DIR = "/nsm/zeek/extracted/complete"
SURICATA_DIR = "/nsm/suripcap/1"
STRELKA_DIR = "/nsm/strelka/processed"

CONFIG_SECTION = "elasticsearch"
REQUIRED_KEYS = ["host", "username", "password"]
CONFIG_PATH = os.path.expanduser("~/.so-mcp/config.ini")


def create_fallback_config(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    config = configparser.ConfigParser()
    config[CONFIG_SECTION] = {key: "" for key in REQUIRED_KEYS}

    with open(path, "w") as f:
        config.write(f)

    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    logger.info(f"Created secure fallback config at {path} (permissions 0600)")


def load_config():
    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_PATH) and os.path.getsize(CONFIG_PATH) > 0:
        config.read(CONFIG_PATH)
        logger.debug(f"Loaded config from: {CONFIG_PATH}")
    else:
        logger.warning("No configuration found.")
        choice = input(f"Would you like to create a new config at {CONFIG_PATH}? [Y/n]: ").strip().lower()
        if choice in ("", "y", "yes"):
            interactive_config()
        else:
            logger.warning("Aborting. Configuration is missing.")
            sys.exit(1)
        # Re-load the newly created config
        config.read(CONFIG_PATH)

    if CONFIG_SECTION not in config:
        logger.error(f"Missing section [{CONFIG_SECTION}] in {CONFIG_PATH}")
        sys.exit(1)

    missing = [key for key in REQUIRED_KEYS if key not in config[CONFIG_SECTION] or not config[CONFIG_SECTION][key].strip()]
    if missing:
        logger.warning(f"Missing keys in config: {', '.join(missing)}")
        choice = input(f"Would you like to fill in the missing fields now? [Y/n]: ").strip().lower()
        if choice in ("", "y", "yes"):
            interactive_config()
            config.read(CONFIG_PATH)  # Reload after editing
        else:
            logger.error("Aborting. Required configuration is incomplete.")
            sys.exit(1)

    return {
        "elasticsearch": {
            "host": config[CONFIG_SECTION]["host"],
            "username": config[CONFIG_SECTION]["username"],
            "password": config[CONFIG_SECTION]["password"],
        }
    }

def interactive_config():
    print(f"[config.py] Configuring values for {CONFIG_PATH}")
    config = configparser.ConfigParser()

    # Ensure the config directory exists
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)

    if CONFIG_SECTION not in config:
        config[CONFIG_SECTION] = {}

    for key in REQUIRED_KEYS:
        existing = config[CONFIG_SECTION].get(key, "").strip()
        if existing:
            print(f"{key} already set.")
            continue
        value = input(f"Enter value for {key}: ").strip()
        config[CONFIG_SECTION][key] = value

    with open(CONFIG_PATH, "w") as f:
        config.write(f)

    os.chmod(CONFIG_PATH, stat.S_IRUSR | stat.S_IWUSR)
    print(f"[config.py] Configuration saved to {CONFIG_PATH} with permissions 0600.")



if __name__ == "__main__":
    interactive_config()
