from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health

from models.songs import SongCreate, SongRead, SongUpdate
from models.artists import ArtistCreate, ArtistRead, ArtistUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
songs: Dict[UUID, SongRead] = {}
artists: Dict[UUID, ArtistRead] = {}

app = FastAPI(
    title="Person/Address API",
    description="Demo FastAPI app using Pydantic v2 models for Person and Address",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    # Each person gets its own UUID; stored as PersonRead
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# Extra endpoints
# -----------------------------------------------------------------------------
# Song endpoints
# -----------------------------------------------------------------------------
@app.post("/songs", response_model=SongRead, status_code=201)
def create_song(song: SongCreate):
    # Each song gets its own UUID; stored as SongRead
    if song.id in songs:
        raise HTTPException(status_code=400, detail="Song with this ID already exists")
    song_read = SongRead(**song.model_dump())
    songs[song_read.id] = song_read
    return song_read

@app.get("/songs", response_model= List[SongRead])
def list_song(
    id: Optional[str] = Query(None, description="Filter by id"),
    name: Optional[str] = Query(None, description="Filter by name"),
    artist_name: Optional[str] = Query(None, description="Filter by name of at least one artist")
):
    results = list(songs.values())

    if id is not None:
        results = [s for s in results if s.id == id]
    if name is not None:
        results = [s for s in results if s.name == name]
    if artist_name is not None:
        results = [s for s in results if any(a.name == artist_name for a in s.artists)]
    return results

@app.get("/songs/{song_id}", response_model=SongRead)
def get_song(song_id: UUID):
    if song_id not in songs:
        raise HTTPException(status_code=404, detail="Song not found")
    return songs[song_id]

@app.patch("/songs/{song_id}", response_model=SongRead)
def update_song(song_id: UUID, update: SongUpdate):
    if song_id not in songs:
        raise HTTPException(status_code=404, detail="Song not found")
    stored = songs[song_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    songs[song_id] = SongRead(**stored)
    return songs[song_id]

@app.delete("/songs/{song_id}", response_model=dict)
def delete_song(song_id: UUID):
    if song_id not in songs:
        raise HTTPException(status_code=404, detail="Song not found")
    deleted_song = songs.pop(song_id)  # remove from dictionary
    return {"detail": f"Song '{deleted_song.name}' was deleted successfully"}

# -----------------------------------------------------------------------------
# Artists endpoints
# -----------------------------------------------------------------------------
@app.post("/artists", response_model=ArtistRead, status_code=201)
def create_artists(artist: ArtistCreate):
    if artist.id in artists:
        raise HTTPException(status_code=400, detail="Artist with this ID already exists")
    artists[artist.id] = ArtistRead(**artist.model_dump())
    return artists[artist.id]

@app.get("/artists", response_model= List[ArtistRead])
def list_artist(
    id: Optional[str] = Query(None, description="Filter by id"),
    name: Optional[str] = Query(None, description="Filter by name"),
):
    results = list(artists.values())
    if id is not None:
        results = [a for a in results if a.id == id]
    if name is not None:
        results = [a for a in results if a.name == name]
    return results

@app.get("/artists/{artist_id}", response_model=ArtistRead)
def get_artist(artist_id: UUID):
    if artist_id not in artists:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artists[artist_id]

@app.patch("/artist/{artist_id}", response_model=ArtistRead)
def update_artist(artist_id: UUID, update: ArtistUpdate):
    if artist_id not in artists:
        raise HTTPException(status_code=404, detail="Artist not found")
    stored = artists[artist_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    artists[artist_id] = ArtistRead(**stored)
    return artists[artist_id]

@app.delete("/artist/{artist_id}", response_model=dict)
def delete_artist(artist_id: UUID):
    if artist_id not in artists:
        raise HTTPException(status_code=404, detail="Artist not found")
    deleted_artist = artists.pop(artist_id)  # remove from dictionary
    return {"detail": f"Artist '{deleted_artist.name}' was deleted successfully"}
# -------------------------------------
# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
