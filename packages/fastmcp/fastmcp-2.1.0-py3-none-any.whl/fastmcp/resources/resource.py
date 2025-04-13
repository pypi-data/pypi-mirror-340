"""Base classes and interfaces for FastMCP resources."""

import abc
from typing import Annotated, Any

from pydantic import (
    AnyUrl,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    UrlConstraints,
    ValidationInfo,
    field_validator,
)
from typing_extensions import Self

from fastmcp.utilities.types import _convert_set_defaults


class Resource(BaseModel, abc.ABC):
    """Base class for all resources."""

    model_config = ConfigDict(validate_default=True)

    uri: Annotated[AnyUrl, UrlConstraints(host_required=False)] = Field(
        default=..., description="URI of the resource"
    )
    name: str | None = Field(description="Name of the resource", default=None)
    description: str | None = Field(
        description="Description of the resource", default=None
    )
    tags: Annotated[set[str], BeforeValidator(_convert_set_defaults)] = Field(
        default_factory=set, description="Tags for the resource"
    )
    mime_type: str = Field(
        default="text/plain",
        description="MIME type of the resource content",
        pattern=r"^[a-zA-Z0-9]+/[a-zA-Z0-9\-+.]+$",
    )

    @field_validator("name", mode="before")
    @classmethod
    def set_default_name(cls, name: str | None, info: ValidationInfo) -> str:
        """Set default name from URI if not provided."""
        if name:
            return name
        if uri := info.data.get("uri"):
            return str(uri)
        raise ValueError("Either name or uri must be provided")

    @abc.abstractmethod
    async def read(self) -> str | bytes:
        """Read the resource content."""
        pass

    def copy(self, updates: dict[str, Any] | None = None) -> Self:
        """Copy the resource with optional updates."""
        data = self.model_dump()
        if updates:
            data.update(updates)
        return type(self)(**data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Resource):
            return False
        return self.model_dump() == other.model_dump()
