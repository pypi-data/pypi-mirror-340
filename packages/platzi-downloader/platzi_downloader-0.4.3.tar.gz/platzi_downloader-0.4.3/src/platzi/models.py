from enum import Enum
from typing import List, Optional
import re

from pydantic import BaseModel
from pydantic.config import ConfigDict


# Implementamos nuestra propia función camelize ya que no está disponible en la versión instalada de humps
def camelize(string):
    """
    Convert a string to camelCase.
    """
    if not string:
        return string
    
    # Split the string by underscores or dashes
    words = re.sub(r'[_-]', ' ', string).split()
    
    # Capitalize all words except the first one
    if len(words) > 0:
        words = [words[0].lower()] + [w.capitalize() for w in words[1:]]
    
    # Join the words back together
    return ''.join(words)


class User(BaseModel):
    model_config = ConfigDict(alias_generator=camelize)

    avatar: str
    name: str
    username: str
    email: str
    user_id: int
    plan: str
    is_authenticated: bool
    user_type: str
    phone_number: str


class TypeUnit(str, Enum):
    LECTURE = "lecture"
    VIDEO = "video"
    QUIZ = "quiz"


class ResourceType(str, Enum):
    FILE = "file"
    LINK = "link"


class Resource(BaseModel):
    name: str
    url: str
    type: ResourceType = ResourceType.FILE


class Video(BaseModel):
    id: int | None = None
    url: str
    subtitles_url: str | None = None
    description: str | None = None
    resources: List[Resource] | None = None
    recommended_readings: List[Resource] | None = None


class Unit(BaseModel):
    id: int | None = None
    type: TypeUnit
    title: str
    url: str
    slug: str
    video: Optional[Video] = None


class Chapter(BaseModel):
    id: int | None = None
    name: str
    slug: str
    description: str | None = None
    units: list[Unit]


class Course(BaseModel):
    id: int | None = None
    name: str
    slug: str
    url: str
    description: str | None = None
    chapters: list[Chapter]
