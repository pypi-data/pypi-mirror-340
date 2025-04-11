import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class Config(BaseModel):
    """config model for api keys and settings."""
    OPENAI_API_KEY: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    TAVILY_API_KEY: str = Field(default_factory=lambda: os.getenv("TAVILY_API_KEY", ""))
    EXA_API_KEY: str = Field(default_factory=lambda: os.getenv("EXA_API_KEY", ""))

    @classmethod
    def load(cls):
        config = cls()
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        if not config.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is required")
        if not config.EXA_API_KEY:
            raise ValueError("EXA_API_KEY is required")
        return config