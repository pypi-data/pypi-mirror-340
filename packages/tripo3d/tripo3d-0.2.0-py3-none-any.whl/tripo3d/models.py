"""
Data models for the Tripo API client.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import datetime


class Animation(str, Enum):
    """Available preset animations for retargeting."""
    IDLE = "preset:idle"
    WALK = "preset:walk"
    CLIMB = "preset:climb"
    JUMP = "preset:jump"
    RUN = "preset:run"
    SLASH = "preset:slash"
    SHOOT = "preset:shoot"
    HURT = "preset:hurt"
    FALL = "preset:fall"
    TURN = "preset:turn"

class ModelStyle(str, Enum):
    """Available styles for model generation."""
    # Person styles
    PERSON_TO_CARTOON = "person:person2cartoon"

    # Animal styles
    ANIMAL_VENOM = "animal:venom"

    # Object styles
    OBJECT_CLAY = "object:clay"
    OBJECT_STEAMPUNK = "object:steampunk"
    OBJECT_CHRISTMAS = "object:christmas"
    OBJECT_BARBIE = "object:barbie"

    # Material styles
    GOLD = "gold"
    ANCIENT_BRONZE = "ancient_bronze"


class PostStyle(str, Enum):
    """Available styles for model postprocessing."""
    # Stylization styles
    LEGO = "lego"
    VOXEL = "voxel"
    VORONOI = "voronoi"
    MINECRAFT = "minecraft"

class TaskStatus(str, Enum):
    """Task status enum."""
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"
    BANNED = "banned"
    EXPIRED = "expired"


@dataclass
class TaskOutput:
    """Task output data."""
    model: Optional[str] = None
    base_model: Optional[str] = None
    pbr_model: Optional[str] = None
    rendered_image: Optional[str] = None
    riggable: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskOutput':
        return cls(
            model=data.get('model'),
            base_model=data.get('base_model'),
            pbr_model=data.get('pbr_model'),
            rendered_image=data.get('rendered_image'),
            riggable=data.get('riggable'),
        )


@dataclass
class Task:
    """Task data model."""
    task_id: str
    type: str
    status: TaskStatus
    input: Dict[str, Any]
    output: TaskOutput
    progress: int
    create_time: int
    running_left_time: Optional[int] = None
    queue_position: Optional[int] = None

    @property
    def created_at(self) -> datetime.datetime:
        """Get the creation time as a datetime object."""
        return datetime.datetime.fromtimestamp(self.create_time)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task from a dictionary."""
        return cls(
            task_id=data['task_id'],
            type=data['type'],
            status=TaskStatus(data['status']),
            input=data['input'],
            output=TaskOutput.from_dict(data['output']),
            progress=data['progress'],
            create_time=data['create_time'],
            running_left_time=data.get('running_left_time'),
            queue_position=data.get('queue_position')
        )


@dataclass
class Balance:
    """User balance data model."""
    balance: float
    frozen: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Balance':
        """Create a Balance from a dictionary."""
        return cls(
            balance=data['balance'],
            frozen=data['frozen']
        )
