import os
import json
import keyring
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

KEYRING_SERVICE = "geegle_cli"

class SecureConfig:
    def __init__(self):
        load_dotenv()
        self.config_dir = Path.home() / ".geegle"
        self.config_path = self.config_dir / "config.json"
        self.config = self._load_config()
        
        self._init_api_keys()
    
    def _load_config(self) -> Dict:
        """Load the configuration file or create default if not exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        
        return {
            "models": {
                "default": "gpt-4-turbo-preview",
                "available": [
                    "gpt-3.5-turbo",
                    "gpt-4-turbo-preview",
                    "gpt-4o",
                    "claude-3-opus-20240229",
                    "claude-3-sonnet-20240229",
                    "claude-3-haiku-20240307"
                ]
            },
            "prompts": {
                "default": "You are a helpful CLI assistant. When provided with web search results, use them to inform your answers.",
                "templates": {
                    "default": "You are a helpful CLI assistant. When provided with web search results, use them to inform your answers.",
                    "concise": "You are a concise CLI assistant that provides brief, factual answers based on search results.",
                    "detailed": "You are a detailed CLI assistant that provides in-depth analysis and comprehensive explanations based on search results.",
                    "coding": "You are a coding expert CLI assistant. Focus on providing working code examples and technical explanations."
                },
            "settings": {
                "use_reranker": True
                }
            },
        }
    
    def _init_api_keys(self):
        """Initialize API keys from environment or keyring."""
        key_names = ["OPENAI_API_KEY", "TAVILY_API_KEY", "EXA_API_KEY", "ANTHROPIC_API_KEY"]
        
        for key_name in key_names:
            env_value = os.getenv(key_name)
            if env_value:
                self.set_api_key(key_name, env_value)
    
    def save(self):
        """Save the config to disk."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        self.config_path.chmod(0o600)
    
    def get_api_key(self, key_name: str) -> Optional[str]:
        """Get an API key from the secure storage."""
        return keyring.get_password(KEYRING_SERVICE, key_name)
    
    def set_api_key(self, key_name: str, value: str):
        """Store an API key in the secure storage."""
        keyring.set_password(KEYRING_SERVICE, key_name, value)
    
    def has_required_keys(self) -> bool:
        """Check if all required API keys are present."""
        required_keys = ["OPENAI_API_KEY", "TAVILY_API_KEY", "EXA_API_KEY"]
        return all(self.get_api_key(key) for key in required_keys)
    
    def get_model_info(self):
        """Get model configuration."""
        return self.config["models"]
    
    def set_default_model(self, model_name: str) -> bool:
        """Set the default model."""
        if model_name in self.config["models"]["available"]:
            self.config["models"]["default"] = model_name
            self.save()
            return True
        return False
    
    def get_prompt_templates(self):
        """Get prompt templates."""
        return self.config["prompts"]["templates"]
    
    def get_default_prompt(self):
        """Get the default prompt."""
        return self.config["prompts"]["default"]
    
    def set_default_prompt(self, prompt: str):
        """Set the default prompt."""
        self.config["prompts"]["default"] = prompt
        self.save()
    
    def add_prompt_template(self, name: str, template: str):
        """Add a new prompt template."""
        self.config["prompts"]["templates"][name] = template
        self.save()
    
    def migrate_from_old_config(self, old_config_path: Optional[Path] = None):
        """Migrate from the old config format to the secure format."""
        if old_config_path is None:
            old_config_path = self.config_dir / "config.json"
        
        if not old_config_path.exists():
            return
        
        try:
            with open(old_config_path, 'r') as f:
                old_config = json.load(f)
            
            for key_name in ["OPENAI_API_KEY", "TAVILY_API_KEY", "EXA_API_KEY", "ANTHROPIC_API_KEY"]:
                if key_name in old_config and old_config[key_name]:
                    self.set_api_key(key_name, old_config[key_name])
            
            if "DEFAULT_MODEL" in old_config:
                self.config["models"]["default"] = old_config["DEFAULT_MODEL"]
            
            if "AVAILABLE_MODELS" in old_config:
                self.config["models"]["available"] = old_config["AVAILABLE_MODELS"]
            
            if "SYSTEM_PROMPT" in old_config:
                self.config["prompts"]["default"] = old_config["SYSTEM_PROMPT"]
            
            if "PROMPT_TEMPLATES" in old_config:
                self.config["prompts"]["templates"] = old_config["PROMPT_TEMPLATES"]
            
            self.save()
            
            backup_path = old_config_path.with_suffix('.json.bak')
            old_config_path.rename(backup_path)
            
            print(f"Successfully migrated configuration. Old config backed up to {backup_path}")
        except Exception as e:
            print(f"Error migrating configuration: {e}")