from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    LITELLM_MODEL: str = "gemini/gemini-1.5-pro-latest"
    GITHUB_TOKEN: str = Field(..., env="GITHUB_TOKEN")
    GITHUB_REPOSITORY: str = Field(..., env="GITHUB_REPOSITORY")
    ISSUE_NUMBER: int = Field(0, env="ISSUE_NUMBER")
    GEMINI_API_KEY: str = Field("", env="GEMINI_API_KEY")
    # OPENAI_API_KEY: str = Field("", env="OPENAI_API_KEY")
    # ANTHROPIC_API_KEY: str = Field("", env="ANTHROPIC_API_KEY")
    # REPOSITORY_SUMMARY_PATH: str = Field("", env="REPOSITORY_SUMMARY_PATH")
    
    YOUR_PERSONAL_ACCESS_TOKEN: str = Field("", env="YOUR_PERSONAL_ACCESS_TOKEN")
    YOUR_PERSONAL_ACCESS_TOKEN_YUKIHIKO: str = Field("", env="YOUR_PERSONAL_ACCESS_TOKEN_YUKIHIKO")
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    # ALLOWED_USERS = ["github-actions[bot]", "Sunwood-ai-labs", "user2"]

@lru_cache()
def get_settings():
    return Settings()
