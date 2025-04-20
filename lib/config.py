import yaml
import os
import sys

def load_config(file_path):
    if not os.path.isfile(file_path):
        sys.exit(f"Error: File not found → {file_path}")

    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as e:
        sys.exit(f"Error: Invalid YAML → {e}")
    except Exception as e:
        sys.exit(f"Error: Could not load config → {e}")

    if not isinstance(config, list):
        sys.exit("Error: Config must be a list of endpoints.")

    for i, ep in enumerate(config):
        if not isinstance(ep, dict):
            sys.exit(f"Error: Endpoint #{i+1} must be a dictionary.")
        if not isinstance(ep.get("name"), str):
            sys.exit(f"Error: Endpoint #{i+1} missing or invalid 'name'.")
        if not isinstance(ep.get("url"), str):
            sys.exit(f"Error: Endpoint #{i+1} missing or invalid 'url'.")

    return config
