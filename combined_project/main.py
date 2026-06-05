from dotenv import load_dotenv
import os

load_dotenv()

class PipelineConfig:
    def __init__(self):
        self.api_url = os.getenv("API_URL")
        self.api_key = os.getenv("API_KEY")
        self.budget_file = os.getenv("BUDGET_FILE")
        self.output_file = os.getenv("OUTPUT_FILE")
        self.log_file = os.getenv("LOG_FILE")
        self.max_retries = os.getenv("MAX_RETRIES")
