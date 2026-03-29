"""Core domain types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Condition:
    """A declarative condition used by exits, events and interactions."""

    type: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Effect:
    """A declarative effect applied to the mutable game state."""

    type: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExitDefinition:
    """A navigable connection between rooms."""

    direction: str
    target: str
    conditions: tuple[Condition, ...] = ()
    failure_text: str | None = None


@dataclass(frozen=True)
class RoomEventDefinition:
    """An event triggered when the player enters a room."""

    conditions: tuple[Condition, ...] = ()
    effects: tuple[Effect, ...] = ()
    text: str | None = None


@dataclass(frozen=True)
class RoomDefinition:
    """A room authored in content data."""

    id: str
    zone: str
    name: str
    aliases: tuple[str, ...]
    first_description: str
    repeat_description: str
    exits: dict[str, ExitDefinition]
    objects: tuple[str, ...]
    scene_id: str | None = None
    tags: tuple[str, ...] = ()
    context_actions: dict[str, str] = field(default_factory=dict)
    context_directions: dict[str, str] = field(default_factory=dict)
    enter_events: tuple[RoomEventDefinition, ...] = ()


@dataclass(frozen=True)
class ObjectDefinition:
    """An authored object or room fixture."""

    id: str
    name: str
    aliases: tuple[str, ...]
    kind: str
    portable: bool
    listed: bool
    location: str
    description: str
    read_text: str | None = None
    initial_visible: bool = True
    initial_states: dict[str, Any] = field(default_factory=dict)
    on_examine_effects: tuple[Effect, ...] = ()
    on_read_effects: tuple[Effect, ...] = ()
    on_take_effects: tuple[Effect, ...] = ()


@dataclass(frozen=True)
class InteractionDefinition:
    """A special command resolution rule."""

    id: str
    action: str
    room_id: str | None = None
    direct_object: str | None = None
    indirect_object: str | None = None
    preposition: str | None = None
    conditions: tuple[Condition, ...] = ()
    effects: tuple[Effect, ...] = ()
    success_text: str | None = None
    failure_text: str | None = None


@dataclass(frozen=True)
class GameDefinition:
    """All static content required to run the game."""

    title: str
    data_version: int
    intro: tuple[str, ...]
    intro_scene: str | None
    start_room: str
    rooms: dict[str, RoomDefinition]
    objects: dict[str, ObjectDefinition]
    interactions: tuple[InteractionDefinition, ...]
    initial_flags: dict[str, bool]


@dataclass
class GameState:
    """Mutable runtime state."""

    current_room_id: str
    inventory: list[str]
    flags: dict[str, bool]
    object_locations: dict[str, str]
    object_states: dict[str, dict[str, Any]]
    visited_rooms: set[str] = field(default_factory=set)
    game_over: bool = False
    exit_requested: bool = False


@dataclass(frozen=True)
class ParsedCommand:
    """Parser output used by the engine."""

    action: str
    raw_text: str
    direct_text: str | None = None
    indirect_text: str | None = None
    preposition: str | None = None
    direction: str | None = None
    error_message: str | None = None

    @property
    def is_error(self) -> bool:
        return self.error_message is not None
