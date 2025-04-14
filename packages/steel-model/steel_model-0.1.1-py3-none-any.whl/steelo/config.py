"""
Base settings.

If there's a .env file in the user's home directory, it will be used.
Otherwise, the .env file in the project root will be used. Environment
variables will override values from .env files.
"""

import os
import sys
import shutil
import logging
import sentry_sdk

from pathlib import Path
from typing import Tuple, Type, ClassVar


from pydantic import DirectoryPath, Field, field_validator, HttpUrl, ValidationError

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    DotEnvSettingsSource,
)
from rich import print as rprint

from steelo.domain import Auto
from steelo.utilities.global_variables import STEEL_PLANT_GEM_DATA_YEAR, PRODUCTION_GEM_DATA_YEARS

logger = logging.getLogger(__name__)
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

sentry_sdk.init(
    dsn="https://efde20e9df4ed1634bd4fba5f998fa53@o4504836894490624.ingest.us.sentry.io/4508448665042945",
    traces_sample_rate=1.0,
)


def get_steelo_home():
    """
    Don't use this function directly. Use settings.root instead. This function is only
    used to be able to set the default value of the steelo home directory and to be
    able to mock it in tests.
    """
    if (steelo_home := os.getenv("STEELO_HOME")) is not None:
        return Path(steelo_home)
    else:
        return Path.home() / ".steelo"


def get_cbc_path() -> Path | None:
    cbc_path = shutil.which("cbc")
    if cbc_path is None:
        logger.warning("cbc not found. Install it with pip install cbc")
        return None
    return Path(cbc_path)


def get_fixtures_dir() -> Path:
    """Get the fixtures directory path."""
    package_dir = Path(__file__).parent
    if (fixtures_dir := package_dir / "fixtures").exists():
        # installed as package (production) -> return ./fixtures
        return fixtures_dir
    else:
        # running from source (development) -> return $PROJECT_ROOT/data/fixtures
        return ROOT_DIR / "data" / "fixtures"


class Settings(BaseSettings):
    """
    Application settings managed by Pydantic BaseSettings.
    """

    project_root: Path = ROOT_DIR
    root: DirectoryPath = Field(default=get_steelo_home(), alias="STEELO_HOME")
    output_dir: DirectoryPath = Field(default=get_steelo_home() / "output")
    steel_plants_csv: Path = Field(
        default=ROOT_DIR / "data" / f"steel_plants_input_data_{STEEL_PLANT_GEM_DATA_YEAR}.csv"
    )
    hist_production_csv: Path = Field(default=ROOT_DIR / "data" / "historical_production_data.csv")
    reg_hist_production_iron_csv: Path = Field(
        default=ROOT_DIR
        / "data"
        / f"iron_production_{PRODUCTION_GEM_DATA_YEARS[0]}to{PRODUCTION_GEM_DATA_YEARS[-1]}.csv"
    )
    reg_hist_production_steel_csv: Path = Field(
        default=ROOT_DIR
        / "data"
        / f"steel_production_{PRODUCTION_GEM_DATA_YEARS[0]}to{PRODUCTION_GEM_DATA_YEARS[-1]}.csv"
    )
    gravity_distances_csv: Path = Field(default=ROOT_DIR / "data" / "gravity_distances.csv")

    # These fields will be set in the __init__ method to use fixtures_dir
    technology_lcop_csv: Path = Auto
    demand_center_xlsx: Path = Auto
    location_csv: Path = Auto
    new_business_cases: Path = Auto
    cost_of_x_csv: Path = Auto

    intermediate_outputs_simulation_run: Path = Field(default=ROOT_DIR / "outputs" / "pam_simulation_run.json")
    geo_boundaries_url: HttpUrl = Field(
        default=HttpUrl("https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson")
    )
    lp_solver_path: Path | None = get_cbc_path()

    # Store fixtures_dir as a class variable
    _fixtures_dir: ClassVar[Path] = get_fixtures_dir()

    def __init__(self, **data):
        # Set defaults for fields that need fixtures_dir before initializing
        if "technology_lcop_csv" not in data:
            data["technology_lcop_csv"] = self._fixtures_dir / "technology_lcop.csv"
        if "demand_center_xlsx" not in data:
            data["demand_center_xlsx"] = self._fixtures_dir / "Data_collection_ultimate_steel.xlsx"
        if "location_csv" not in data:
            data["location_csv"] = self._fixtures_dir / "countries.csv"
        if "new_business_cases" not in data:
            data["new_business_cases"] = self._fixtures_dir / "2024_12_13_New business cases_MVP.xlsx"
        if "cost_of_x_csv" not in data:
            data["cost_of_x_csv"] = self._fixtures_dir / "cost_of_x.json"
        if "gravity_distances_csv" not in data:
            data["gravity_distances_csv"] = self._fixtures_dir / "gravity_distances.csv"

        super().__init__(**data)

    @field_validator("root", "output_dir", mode="before")
    def path_must_exist_or_create(cls, path: DirectoryPath) -> DirectoryPath:
        """Ensure the path exists or create it."""
        path.mkdir(parents=True, exist_ok=True)
        return DirectoryPath(path)

    model_config = SettingsConfigDict(extra="ignore")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Determine the appropriate .env file"""
        home_env = get_steelo_home() / ".env"
        project_env = ROOT_DIR / ".env"
        if home_env.exists():
            env_file = home_env
        else:
            env_file = project_env

        # Create a new DotEnvSettingsSource with the selected env_file
        new_dotenv_settings = DotEnvSettingsSource(
            settings_cls=settings_cls,
            env_file=env_file,
            env_file_encoding="utf-8",
        )

        # Return the sources in the desired order
        return (
            init_settings,
            env_settings,
            new_dotenv_settings,
            file_secret_settings,
        )

    @property
    def sample_plants_json_path(self) -> Path:
        return self._fixtures_dir / "plants.json"

    @property
    def sample_demand_center_json_path(self) -> Path:
        return self._fixtures_dir / "demand_center.json"


try:
    settings = Settings()
except ValidationError as e:
    rprint("validation error: ", e)
    sys.exit(1)
