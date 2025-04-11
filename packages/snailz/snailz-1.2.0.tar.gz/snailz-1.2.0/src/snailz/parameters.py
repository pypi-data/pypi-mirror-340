"""Parameter classes."""

from datetime import date
import faker.config

from pydantic import BaseModel, Field, field_validator, model_validator

from . import utils


# Default locale for name generation
DEFAULT_LOCALE = "et_EE"

# Default size for assay plates
DEFAULT_PLATE_SIZE = 4

# Default starting date for surveys
DEFAULT_START_DATE = date.fromisoformat("2024-03-01")


class AssayParams(BaseModel):
    """Parameters for assay generation."""

    baseline: float = Field(default=1.0, ge=0.0, description="Baseline reading value")
    degrade: float = Field(
        default=0.05,
        ge=0.0,
        le=1.0,
        description="Rate at which sample responses decrease per day after first day (0..1)",
    )
    delay: int = Field(
        default=5,
        gt=0,
        description="Maximum number of days between specimen collection and assay",
    )
    mutant: float = Field(
        default=5.0, gt=0.0, description="Mutant reading value (must be positive)"
    )
    reading_noise: float = Field(
        default=0.2, ge=0.0, description="Noise level for readings (must be positive)"
    )
    plate_size: int = Field(
        default=DEFAULT_PLATE_SIZE,
        gt=0,
        description="Size of assay plate (must be positive)",
    )
    image_noise: int = Field(
        default=32,
        ge=0,
        le=255,
        description="Plate image noise (grayscale 0-255)",
    )
    p_duplicate_assay: float = Field(
        default=0.05, ge=0, description="Probably that an assay is repeated"
    )

    model_config = {"extra": "forbid"}

    @model_validator(mode="after")
    def validate_fields(self):
        """Validate requirements on fields."""
        if self.mutant < self.baseline:
            raise ValueError("mutant value must be greater than baseline")
        return self


class MachineParams(BaseModel):
    """Parameters for machine generation."""

    number: int = Field(default=5, gt=0, description="Number of machines")
    variation: float = Field(default=0.15, ge=0, description="Camera variation")

    model_config = {"extra": "forbid"}


class PersonParams(BaseModel):
    """Parameters for people generation."""

    locale: str = Field(default=DEFAULT_LOCALE, description="Locale for names")
    number: int = Field(default=5, gt=0, description="Number of people")

    model_config = {"extra": "forbid"}

    @field_validator("locale")
    def validate_fields(cls, v):
        """Validate that the locale is available in faker."""
        if v not in faker.config.AVAILABLE_LOCALES:
            raise ValueError(f"Unknown locale {v}")
        return v


class SpecimenParams(BaseModel):
    """Parameters for specimen generation."""

    length: int = Field(
        default=20, gt=0, description="Length of specimen genomes (must be positive)"
    )
    start_date: date = Field(
        default=DEFAULT_START_DATE,
        description="Start date for specimen collection",
    )
    max_mass: float = Field(
        default=10.0, gt=0, description="Maximum mass for specimens (must be positive)"
    )
    mut_mass_scale: float = Field(
        default=2.0, gt=0, description="Scaling factor for mutant snail mass"
    )
    num_mutations: int = Field(
        default=5,
        ge=0,
        description="Number of mutations in specimens (must be between 0 and length)",
    )
    spacing: float = Field(
        default=utils.DEFAULT_SURVEY_SIZE / 4.0,
        ge=0,
        description="Inter-specimen spacing",
    )
    daily_growth: float = Field(
        default=0.01,
        ge=0,
        description="Mass increase per day",
    )
    p_missing_location: float = Field(
        default=0.05, ge=0, description="Probability that location is missing"
    )

    model_config = {"extra": "forbid"}


class SurveyParams(BaseModel):
    """Parameters for survey generation."""

    number: int = Field(default=3, gt=0, description="Number of surveys")
    size: int = Field(
        default=utils.DEFAULT_SURVEY_SIZE, gt=0, description="Survey size"
    )
    start_date: date = Field(
        default=DEFAULT_START_DATE,
        description="Start date for specimen collection",
    )
    max_interval: int = Field(
        gt=0, default=7, description="Maximum interval between samples"
    )

    model_config = {"extra": "forbid"}


class ScenarioParams(BaseModel):
    """Represent all parameters combined."""

    seed: int = Field(default=7493418, ge=0, description="RNG seed")
    assay: AssayParams = Field(
        default=AssayParams(), description="parameters for assay generation"
    )
    machine: MachineParams = Field(
        default=MachineParams(), description="parameters for machine generation"
    )
    person: PersonParams = Field(
        default=PersonParams(), description="parameters for people generation"
    )
    specimen: SpecimenParams = Field(
        default=SpecimenParams(),
        description="parameters for specimen generation",
    )
    survey: SurveyParams = Field(
        default=SurveyParams(), description="parameters for survey generation"
    )

    model_config = {"extra": "forbid"}
