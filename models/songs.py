from __future__ import annotations

from pydantic import BaseModel, Field, EmailStr, StringConstraints
from typing import Optional
from datetime import timedelta

class Song(BaseModel):
    name: str = Field(description="String format")
    artist: str = Field(description="String format")
    length: timedelta = Field(description="Song duration as a timedelta")
    created_at: str = Field(description="Time in ISO 8601 format (UTC)")
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Save Your Tears",
                "artist": "The Weekend",
                "length": "PT3M36S",
                "created_at": "2025-09-11T22:45:00Z"
            }
        }
    }

class Artist(BaseModel):
    name: str = Field(description="String format")
    real_name: Optional[str] = Field(default=None, description="Real name if applicable")
    bio: Optional[str] = Field(default=None, description="Description if applicable")
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "The Weekend",
                "real_name": "Abel Tesfaye",
                "bio": "born February 16, 1990, in Toronto"
            }
        }
    }