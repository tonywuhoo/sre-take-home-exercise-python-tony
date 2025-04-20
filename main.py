import os
import sys
import logging
from datetime import datetime
from lib.config import load_config
from lib.monitor import monitor_endpoints

os.makedirs("logs", exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"logs/health_check_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        config = load_config(config_file)
        monitor_endpoints(config)
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)
