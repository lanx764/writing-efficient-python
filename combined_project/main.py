from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os
import logging
import sys

load_dotenv()

class PipelineConfig:
    def __init__(self):
        self.api_url = os.getenv("API_URL")
        self.api_key = os.getenv("API_KEY")
        self.budget_file = os.getenv("BUDGET_FILE")
        self.output_file = os.getenv("OUTPUT_FILE")
        self.log_file = os.getenv("LOG_FILE")
        self.max_retries = int(os.getenv("MAX_RETRIES"))

def validate_env(config):
    required = {
        "API_URL": config.api_url,
        "API_KEY": config.api_key,
        "BUDGET_FILE": config.budget_file,
        "OUTPUT_FILE": config.output_file,
        "LOG_FILE": config.log_file,
        "MAX_RETRIES": config.max_retries,
    }

    missing_variables = [key for key,val in required.items() if not val]

    if missing_variables:
        raise EnvironmentError(f"Missing required environment variables: '{', '.join(missing_variables)}'")

def get_logger(name):
    logger =logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(fmt='%(asctime)s | %(name)s | %(levelname)s | %(funcName)s | %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    rotating_handler = RotatingFileHandler(filename="pipeline.log",maxBytes=1024,backupCount=3)
    rotating_handler.setLevel(logging.DEBUG)
    rotating_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(rotating_handler)
    logger.propagate = False

    return logger

class PipelineError(Exception):
    pass

class APIError(PipelineError):
    pass

class ValidationError(PipelineError):
    pass

class TransformError(PipelineError):
    pass


