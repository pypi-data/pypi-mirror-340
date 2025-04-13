"""
NOVA: The Prompt Pattern Matching
Author: Thomas Roccia 
twitter: @fr0gger_
License: MIT License
Version: 1.0.0
Description: Configuration utilities for Nova framework
"""

import os
import json
import configparser
from typing import Dict, Any, Optional


class NovaConfig:
    """Configuration manager for Nova framework."""
    
    DEFAULT_CONFIG_PATHS = [
        os.path.expanduser("~/.nova/config.ini"),
        os.path.join(os.getcwd(), "nova.ini"),
    ]
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to config file (optional)
        """
        self.config = {}
        self.config_path = config_path
        
        # Load configuration
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file and environment variables."""
        # Start with default config
        self.config = {
            "llm": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "timeout": 10
            },
            "semantics": {
                "model": "all-MiniLM-L6-v2",
                "cache_embeddings": True
            },
            "logging": {
                "level": "INFO",
                "file": None
            }
        }
        
        # Load from config file if available
        if self.config_path:
            self._load_from_file(self.config_path)
        else:
            # Try default paths
            for path in self.DEFAULT_CONFIG_PATHS:
                if os.path.exists(path):
                    self._load_from_file(path)
                    break
        
        # Override with environment variables
        self._load_from_env()
    
    def _load_from_file(self, path: str):
        """Load configuration from file."""
        try:
            if path.endswith('.json'):
                with open(path, 'r') as f:
                    file_config = json.load(f)
                    self._merge_config(file_config)
            else:
                # Assume INI format
                parser = configparser.ConfigParser()
                parser.read(path)
                
                for section in parser.sections():
                    if section not in self.config:
                        self.config[section] = {}
                    
                    for key, value in parser.items(section):
                        # Convert types
                        if value.lower() in ('true', 'yes', '1'):
                            value = True
                        elif value.lower() in ('false', 'no', '0'):
                            value = False
                        elif value.isdigit():
                            value = int(value)
                        elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                            value = float(value)
                        
                        self.config[section][key] = value
        except Exception as e:
            print(f"Error loading config from {path}: {e}")
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # LLM configuration
        if os.environ.get("NOVA_LLM_PROVIDER"):
            self.config["llm"]["provider"] = os.environ["NOVA_LLM_PROVIDER"]
        
        if os.environ.get("NOVA_LLM_MODEL"):
            self.config["llm"]["model"] = os.environ["NOVA_LLM_MODEL"]
        
        # API keys
        for provider in ["OPENAI", "ANTHROPIC", "AZURE_OPENAI"]:
            env_var = f"{provider}_API_KEY"
            if os.environ.get(env_var):
                if "api_keys" not in self.config:
                    self.config["api_keys"] = {}
                self.config["api_keys"][provider.lower()] = os.environ[env_var]
        
        # Semantic model
        if os.environ.get("NOVA_SEMANTIC_MODEL"):
            self.config["semantics"]["model"] = os.environ["NOVA_SEMANTIC_MODEL"]
    
    def _merge_config(self, new_config: Dict[str, Any]):
        """Merge new configuration into existing config."""
        for section, values in new_config.items():
            if isinstance(values, dict):
                if section not in self.config:
                    self.config[section] = {}
                
                for key, value in values.items():
                    self.config[section][key] = value
            else:
                self.config[section] = values
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(section, {}).get(key, default)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Configuration section
            
        Returns:
            Dictionary of section values or empty dict if section not found
        """
        return self.config.get(section, {})
    
    def set(self, section: str, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
    
    def save(self, path: Optional[str] = None):
        """
        Save configuration to file.
        
        Args:
            path: Path to save config to (defaults to loaded path)
        """
        save_path = path or self.config_path
        if not save_path:
            raise ValueError("No config path specified")
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            if save_path.endswith('.json'):
                with open(save_path, 'w') as f:
                    json.dump(self.config, f, indent=2)
            else:
                # Save as INI
                parser = configparser.ConfigParser()
                
                for section, values in self.config.items():
                    if isinstance(values, dict):
                        parser[section] = {}
                        for key, value in values.items():
                            parser[section][key] = str(value)
                    else:
                        # Handle non-dict sections
                        parser["DEFAULT"][section] = str(values)
                
                with open(save_path, 'w') as f:
                    parser.write(f)
                    
            print(f"Configuration saved to {save_path}")
            
        except Exception as e:
            print(f"Error saving config to {save_path}: {e}")
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return json.dumps(self.config, indent=2)


# Global configuration instance
_config = None


def get_config(config_path: Optional[str] = None) -> NovaConfig:
    """
    Get global configuration instance.
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        NovaConfig instance
    """
    global _config
    if _config is None or config_path:
        _config = NovaConfig(config_path)
    
    return _config