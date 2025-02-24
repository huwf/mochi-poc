import uuid
from uuid import UUID

from pydantic import BaseModel, default_factory, HttpUrl


class Media(BaseModel):
    uid: UUID = default_factory(uuid.uuid4)
    filename: str
    source: HttpUrl
    pretty_name: str
    file_format: str

