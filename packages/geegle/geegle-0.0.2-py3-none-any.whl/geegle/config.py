import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


load_dotenv()

class Config(BaseModel):
    """config model for api keys and settings."""
    OPENAI_API_KEY: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    TAVILY_API_KEY: str = Field(default_factory=lambda: os.getenv("TAVILY_API_KEY", ""))
    EXA_API_KEY: str = Field(default_factory=lambda: os.getenv("EXA_API_KEY", ""))
    
    DEFAULT_MODEL: str = Field(default="gpt-4-turbo-preview")
    AVAILABLE_MODELS: List[str] = Field(default_factory=lambda: [
        "gpt-3.5-turbo",
        "gpt-4-turbo-preview",
        "gpt-4o",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ])
    
    SYSTEM_PROMPT: str = Field(
        default="You are a helpful CLI assistant. When provided with web search results, use them to inform your answers."
    )
    PROMPT_TEMPLATES: Dict[str, str] = Field(default_factory=lambda: {
        "default": "You are a helpful CLI assistant. When provided with web search results, use them to inform your answers.",
        "concise": "You are a concise CLI assistant that provides brief, factual answers based on search results.",
        "detailed": "You are a detailed CLI assistant that provides in-depth analysis and comprehensive explanations based on search results.",
        "coding": "You are a coding expert CLI assistant. Focus on providing working code examples and technical explanations."
    })

    @classmethod
    def load(cls):
        config = cls()
        config_path = Path.home() / ".geegle" / "config.json"
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                saved_config = json.load(f)
                for field in config.__fields__:
                    if field in saved_config:
                        setattr(config, field, saved_config[field])
        
        if not all([config.OPENAI_API_KEY, config.TAVILY_API_KEY, config.EXA_API_KEY]):
            config_path.parent.mkdir(parents=True, exist_ok=True)
            print("First-time setup: API keys required")
            
            if not config.OPENAI_API_KEY:
                config.OPENAI_API_KEY = input("Enter your OpenAI API key: ")
            if not config.TAVILY_API_KEY:
                config.TAVILY_API_KEY = input("Enter your Tavily API key: ")
            if not config.EXA_API_KEY:
                config.EXA_API_KEY = input("Enter your Exa API key: ")
                
            # Save to config file
            config._save_config(config_path)
            
            print("Configuration saved to ~/.geegle/config.json")
        
        return config
    
    def _save_config(self, config_path: Optional[Path] = None):
        """Save the current configuration to a file."""
        if config_path is None:
            config_path = Path.home() / ".geegle" / "config.json"
            
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(self.dict(), f, indent=2)
    
    def update_system_prompt(self, prompt: str) -> None:
        """Update the system prompt and save the configuration."""
        self.SYSTEM_PROMPT = prompt
        self._save_config()
    
    def set_model(self, model: str) -> bool:
        """Set the default model if it's in the available models list."""
        if model in self.AVAILABLE_MODELS:
            self.DEFAULT_MODEL = model
            self._save_config()
            return True
        return False
    
    def add_prompt_template(self, name: str, template: str) -> None:
        """Add or update a prompt template."""
        self.PROMPT_TEMPLATES[name] = template
        self._save_config()
    
    def remove_prompt_template(self, name: str) -> bool:
        """Remove a prompt template if it exists and is not the default."""
        if name in self.PROMPT_TEMPLATES and name != "default":
            del self.PROMPT_TEMPLATES[name]
            self._save_config()
            return True
        return False
    
    def use_prompt_template(self, template_name: str) -> bool:
        """Set the system prompt from a template."""
        if template_name in self.PROMPT_TEMPLATES:
            self.SYSTEM_PROMPT = self.PROMPT_TEMPLATES[template_name]
            self._save_config()
            return True
        return False