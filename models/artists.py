from __future__ import annotations

from pydantic import BaseModel, Field, EmailStr, StringConstraints
from typing import Optional
from datetime import datetime, timedelta
from uuid import UUID, uuid4


class ArtistBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    name: str = Field(description="String format")
    real_name: Optional[str] = Field(default=None, description="Real name if applicable")
    bio: Optional[str] = Field(default=None, description="Description if applicable")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id":"650e8400-e29b-41d4-a716-446655440000",
                    "name": "The Weekend",
                    "real_name": "Abel Tesfaye",
                    "bio": "born February 16, 1990, in Toronto"
                }
            ]
        }
    }

class ArtistCreate(ArtistBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id":"650e8400-e29b-41d4-a716-446655440000",
                    "name": "The Weekend",
                    "real_name": "Abel Tesfaye",
                    "bio": "born February 16, 1990, in Toronto"
                }
            ]
        }
    }

class ArtistUpdate(ArtistBase):
    name: str = Field(description="String format")
    real_name: Optional[str] = Field(default=None, description="Real name if applicable")
    bio: Optional[str] = Field(default=None, description="Description if applicable")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id":"650e8400-e29b-41d4-a716-446655440000",
                    "name": "The Weekend",
                    "real_name": "Abel Tesfaye",
                    "bio": "born February 16, 1990, in Toronto"
                }
            ]
        }
    }

class ArtistRead(ArtistBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id":"650e8400-e29b-41d4-a716-446655440000",
                    "name": "The Weekend",
                    "real_name": "Abel Tesfaye",
                    "bio": "born February 16, 1990, in Toronto",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }