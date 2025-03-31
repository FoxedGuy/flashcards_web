from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Flashcards"
    db_host: str = "db"
    db_port: str = "5432"
    db_user: str = "flash"
    db_password: str = "flash"
    db_name: str = "flashcards"

    root_path: str = ""

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
