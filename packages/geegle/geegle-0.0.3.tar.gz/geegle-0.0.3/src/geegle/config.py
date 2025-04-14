from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import gc

from geegle.secure_config import SecureConfig

load_dotenv()

class Config(BaseModel):
    DEFAULT_MODEL: str = Field(default="gpt-4-turbo-preview")
    AVAILABLE_MODELS: List[str] = Field(default_factory=lambda: [
        "gpt-3.5-turbo",
        "gpt-4-turbo-preview",
        "gpt-4o",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ])

    USE_RERANKER: bool = Field(default=False)
    
    SYSTEM_PROMPT: str = Field(
        default="You are a helpful CLI assistant. When provided with web search results, use them to inform your answers."
    )
    PROMPT_TEMPLATES: Dict[str, str] = Field(default_factory=lambda: {
        "default": "You are a helpful CLI assistant. When provided with web search results, use them to inform your answers.",
        "concise": "You are a concise CLI assistant that provides brief, factual answers based on search results.",
        "detailed": "You are a detailed CLI assistant that provides in-depth analysis and comprehensive explanations based on search results.",
        "coding": "You are a coding expert CLI assistant. Focus on providing working code examples and technical explanations."
    })
    
    _secure_config: Optional[SecureConfig] = None

    @property
    def OPENAI_API_KEY(self) -> str:
        return self._get_api_key("OPENAI_API_KEY")
    
    @OPENAI_API_KEY.setter
    def OPENAI_API_KEY(self, value: str):
        self._set_api_key("OPENAI_API_KEY", value)
    
    @property
    def TAVILY_API_KEY(self) -> str:
        return self._get_api_key("TAVILY_API_KEY")
    
    @TAVILY_API_KEY.setter
    def TAVILY_API_KEY(self, value: str):
        self._set_api_key("TAVILY_API_KEY", value)
    
    @property
    def EXA_API_KEY(self) -> str:
        return self._get_api_key("EXA_API_KEY")
    
    @EXA_API_KEY.setter
    def EXA_API_KEY(self, value: str):
        self._set_api_key("EXA_API_KEY", value)
    
    @property
    def ANTHROPIC_API_KEY(self) -> str:
        return self._get_api_key("ANTHROPIC_API_KEY")
    
    @ANTHROPIC_API_KEY.setter
    def ANTHROPIC_API_KEY(self, value: str):
        self._set_api_key("ANTHROPIC_API_KEY", value)
    
    def _get_api_key(self, key_name: str) -> str:
        """Get an API key from secure storage."""
        if self._secure_config is None:
            self._secure_config = SecureConfig()
        
        return self._secure_config.get_api_key(key_name) or ""
    
    def _set_api_key(self, key_name: str, value: str):
        """Set an API key in secure storage."""
        if self._secure_config is None:
            self._secure_config = SecureConfig()
        
        self._secure_config.set_api_key(key_name, value)
        value = "x" * len(value)
        del value
        gc.collect() 

    @classmethod
    def load(cls):
        config = cls()
        
        secure_config = SecureConfig()
        secure_config.migrate_from_old_config()
        config._secure_config = secure_config
        
        model_info = secure_config.get_model_info()
        config.DEFAULT_MODEL = model_info["default"]
        config.AVAILABLE_MODELS = model_info["available"]
        
        config.SYSTEM_PROMPT = secure_config.get_default_prompt()
        config.PROMPT_TEMPLATES = secure_config.get_prompt_templates()
        
        if not secure_config.has_required_keys():
            print("Required API keys are missing. Please enter them now:")
            
            if not config.OPENAI_API_KEY:
                openai_key = input("Enter your OpenAI API key: ")
                config.OPENAI_API_KEY = openai_key
            
            if not config.TAVILY_API_KEY:
                tavily_key = input("Enter your Tavily API key: ")
                config.TAVILY_API_KEY = tavily_key
            
            if not config.EXA_API_KEY:
                exa_key = input("Enter your Exa API key: ")
                config.EXA_API_KEY = exa_key
                
            print("API keys stored securely in your system keychain")

        config.USE_RERANKER = secure_config.config.get("settings", {}).get("use_reranker", False)

        return config
    
    def _save_config(self):
        if self._secure_config is None:
            self._secure_config = SecureConfig()
        
        model_info = self._secure_config.get_model_info()
        model_info["default"] = self.DEFAULT_MODEL
        model_info["available"] = self.AVAILABLE_MODELS
        
        self._secure_config.set_default_prompt(self.SYSTEM_PROMPT)
        for name, template in self.PROMPT_TEMPLATES.items():
            self._secure_config.add_prompt_template(name, template)
        
        self._secure_config.config["settings"] = {
            "use_reranker": self.USE_RERANKER
        }
        
        self._secure_config.save()
    
    def update_system_prompt(self, prompt: str) -> None:
        self.SYSTEM_PROMPT = prompt
        self._save_config()
    
    def get_model_provider(self, model: str) -> str:
        if model.startswith("gpt") or model.startswith("text-"):
            return "openai"
        elif model.startswith("claude"):
            return "anthropic"
        else:
            return "unknown"
    
    def has_required_api_key(self, model: str) -> bool:
        provider = self.get_model_provider(model)
        if provider == "openai":
            return bool(self.OPENAI_API_KEY)
        elif provider == "anthropic":
            return bool(self.ANTHROPIC_API_KEY)
        else:
            return False
    
    def set_model(self, model: str) -> bool:
        if model in self.AVAILABLE_MODELS:
            self.DEFAULT_MODEL = model
            self._save_config()
            return True
        return False
    
    def add_prompt_template(self, name: str, template: str) -> None:
        self.PROMPT_TEMPLATES[name] = template
        self._save_config()
    
    def remove_prompt_template(self, name: str) -> bool:
        if name in self.PROMPT_TEMPLATES and name != "default":
            del self.PROMPT_TEMPLATES[name]
            self._save_config()
            return True
        return False
    
    def use_prompt_template(self, template_name: str) -> bool:
        if template_name in self.PROMPT_TEMPLATES:
            self.SYSTEM_PROMPT = self.PROMPT_TEMPLATES[template_name]
            self._save_config()
            return True
        return False