from typing import Tuple, Type, Optional

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PyprojectTomlConfigSettingsSource,
    PydanticBaseSettingsSource,
)

from src.models.connection import KafkaMeta


class ApplicationConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    kafka: KafkaMeta


class ProjectConfig(BaseSettings):

    name: str
    version: str = "0.1.0"
    description: str = ""
    authors: list[dict] = []

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (PyprojectTomlConfigSettingsSource(settings_cls),)

    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("project",), extra="ignore"
    )

    @property
    def title(self) -> str:
        return self.name.replace("-", " ").title()
