import logging
import yaml

with open("application.yaml", "r") as f:
    config = yaml.safe_load(f)

log_level = config.get("log_level", "INFO").upper()

logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

def get_logger(name):
    return logging.getLogger(name)
