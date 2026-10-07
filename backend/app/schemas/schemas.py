"""Pydantic v2 Schemas and Contracts for Sortify API."""

from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

# Canonical 5 waste categories and corresponding color associations
ALLOWED_CATEGORIES: set[str] = {"compost", "glass", "landfill", "paper", "plastic"}

BIN_COLORS: dict[str, str] = {
    "compost": "Green",
    "glass": "Teal",
    "landfill": "Gray",
    "paper": "Brown",
    "plastic": "Blue",
}


class ClassificationAlternative(BaseModel):
    """Secondary classification prediction candidate."""

    category: str
    confidence: float = Field(..., ge=0.0, le=1.0)

    @field_validator("category", mode="before")
    @classmethod
    def validate_category(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("Category must be a string")
        normalized = value.strip().lower()
        if normalized not in ALLOWED_CATEGORIES:
            raise ValueError(
                f"Invalid category '{value}'. Must be one of {sorted(ALLOWED_CATEGORIES)}"
            )
        return normalized

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {value}")
        return round(float(value), 4)


class DisposalTip(BaseModel):
    """Specific disposal instructions for a waste item."""

    action: str
    bin_type: str
    notes: str | None = None


class ClassifyResponse(BaseModel):
    """API response model for item classification."""

    item_name: str
    category: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    disposal_tip: str = ""
    bin_color: str = ""
    bin: str | None = None
    disposal_tips: DisposalTip | None = None
    alternatives: list[ClassificationAlternative] = Field(default_factory=list)
    location: str = "berkeley"

    @field_validator("category", mode="before")
    @classmethod
    def validate_category(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("Category must be a string")
        normalized = value.strip().lower()
        if normalized not in ALLOWED_CATEGORIES:
            raise ValueError(
                f"Invalid category '{value}'. Must be one of {sorted(ALLOWED_CATEGORIES)}"
            )
        return normalized

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {value}")
        return round(float(value), 4)

    @model_validator(mode="after")
    def populate_defaults_and_helpers(self) -> "ClassifyResponse":
        category_norm = self.category.lower()
        canonical_color = BIN_COLORS.get(category_norm, "Green")

        if not self.bin_color:
            self.bin_color = canonical_color

        if not self.disposal_tip:
            self.disposal_tip = f"Place in the {self.bin_color} bin."

        if not self.bin:
            self.bin = f"{self.bin_color} {self.category.capitalize()} Bin"

        if self.disposal_tips is None:
            self.disposal_tips = DisposalTip(
                action=self.disposal_tip,
                bin_type=self.bin_color.lower(),
                notes=f"Accepted under {self.location} municipal recycling guidelines.",
            )

        return self


class RuleResponse(BaseModel):
    """API response model for city-specific disposal rules."""

    city: str
    rules: dict[str, str]
    source_url: str

    @field_validator("city", mode="before")
    @classmethod
    def validate_city(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("City must be a string")
        if not value.strip():
            raise ValueError("City must be a non-empty string")
        return value.strip().lower()


class ScanRecord(BaseModel):
    """User scan history record model."""

    scan_id: str
    user_id: str
    timestamp: str
    category: str
    item_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    location: str | None = "berkeley"
    bin_color: str | None = None

    @field_validator("category", mode="before")
    @classmethod
    def validate_category(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("Category must be a string")
        normalized = value.strip().lower()
        if normalized not in ALLOWED_CATEGORIES:
            raise ValueError(
                f"Invalid category '{value}'. Must be one of {sorted(ALLOWED_CATEGORIES)}"
            )
        return normalized

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {value}")
        return round(float(value), 4)

    @model_validator(mode="after")
    def set_default_bin_color(self) -> "ScanRecord":
        if not self.bin_color:
            self.bin_color = BIN_COLORS.get(self.category.lower(), "Green")
        return self
