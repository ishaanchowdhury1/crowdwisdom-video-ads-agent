from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    apify_api_token: str = os.getenv("APIFY_API_TOKEN", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    exa_api_key: str = os.getenv("EXA_API_KEY", "")
    crowdwisdom_url: str = os.getenv("CROWDWISDOM_URL", "https://www.crowdwisdomtrading.com/")
    hermes_model: str = os.getenv("HERMES_MODEL", "openrouter/auto")

settings = Settings()
