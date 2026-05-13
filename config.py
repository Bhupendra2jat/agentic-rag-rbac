from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    chroma_persist_directory: str = "./chroma_db"
    ollama_model: str = "llama3"
    valid_roles: list[str] = ["junior", "executive", "director"]

    class Config:
        env_file = ".env"

settings = Settings()