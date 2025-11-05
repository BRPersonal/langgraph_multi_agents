from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
  GROQ_API_KEY : str
  OPENAI_API_KEY: str
  DEFAULT_MODEL: str
  max_retries: int = 3

  model_config = {"env_file": ".env"}
  

# Global singleton instance
settings = Settings()

# Ensure the environment variable is set for libraries that need it
# This is actually a bad design from openai - burying env variables 
# names deep inside their libraries
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

