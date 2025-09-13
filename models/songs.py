from __future__ import annotations

from pydantic import BaseModel, Field, EmailStr, StringConstraints
from typing import Optional, List
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from .artists import ArtistBase

class SongBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    name: str = Field(description="String format")
    # Embed artists (each with persistent ID), the order will indicate the ownership of the song
    artists: List[ArtistBase] = Field(
        default_factory=list,
        description="Artists linked to this song maybe collaboration (each carries a persistent Artist ID)",
        json_schema_extra= {
            "example": [
                {
                    "id":"123-123",
                    "name": "The Weekend",
                    "real_name": "Abel Tesfaye",
                    "bio": "born February 16, 1990, in Toronto"
                }
            ]
        }
    )
    length: timedelta = Field(description="Song duration as a timedelta")
    published_date: str = Field(description="Time in ISO 8601 format (UTC)")
    model_config = {
        "json_schema_extra": {
            "example": {
                "uid":"123-123",
                "name": "Save Your Tears",
                "artists": [
                    {
                        "id":"123-123",
                        "name": "The Weekend",
                        "real_name": "Abel Tesfaye",
                        "bio": "born February 16, 1990, in Toronto"
                    }
                ],
                "length": "PT3M36S",
                "created_at": "2025-09-11T22:45:00Z"
            }
        }
    }

class SongCreate(SongBase):
    """Creation payload for a Song."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "uid":"123-123",
                "name": "Save Your Tears",
                "artists": [
                    {
                        "id":"123-123",
                        "name": "The Weekend",
                        "real_name": "Abel Tesfaye",
                        "bio": "born February 16, 1990, in Toronto"
                    }
                ],
                "length": "PT3M36S",
                "created_at": "2025-09-11T22:45:00Z"
            }
        }
    }

class SongUpdate(SongBase):
    name: Optional[str] = Field(description="String format")
    artists: Optional[List[ArtistBase]] = Field(
        default_factory=list,
        description="Artists linked to this song maybe collaboration (each carries a persistent Artist ID)",
        json_schema_extra= {
            "example": [
                {
                    "id":"123-123",
                    "name": "The Weekend",
                    "real_name": "Abel Tesfaye",
                    "bio": "born February 16, 1990, in Toronto"
                }
            ]
        }
    )
    length: Optional[timedelta] = Field(description="Song duration as a timedelta")
    published_date: Optional[str] = Field(description="Time in ISO 8601 format (UTC)")
    model_config = {
        "json_schema_extra": {
            "example": {
                "uid":"123-123",
                "name": "Save Your Tears",
                "artists": [
                    {
                        "id":"123-123",
                        "name": "The Weekend",
                        "real_name": "Abel Tesfaye",
                        "bio": "born February 16, 1990, in Toronto"
                    }
                ],
                "length": "PT3M36S",
                "created_at": "2025-09-11T22:45:00Z"
            }
        }
    }

class SongRead(SongBase):
    id: UUID = Field(
        default_factory=uuid4,
        description="ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
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
            "example": {
                "uid":"123-123",
                "name": "Save Your Tears",
                "artists": [
                    {
                        "id":"123-123",
                        "name": "The Weekend",
                        "real_name": "Abel Tesfaye",
                        "bio": "born February 16, 1990, in Toronto"
                    }
                ],
                "length": "PT3M36S",
                "created_at": "2025-09-11T22:45:00Z"
            }
        }
    }
