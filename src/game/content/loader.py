"""JSON content loading."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from game.model import (
    Condition,
    Effect,
    ExitDefinition,
    GameDefinition,
    InteractionDefinition,
    ObjectDefinition,
    RoomDefinition,
    RoomEventDefinition,
)

from .validator import validate_definition


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _condition_from_dict(raw: dict[str, Any]) -> Condition:
    payload = {key: value for key, value in raw.items() if key != "type"}
    return Condition(type=raw["type"], payload=payload)


def _effect_from_dict(raw: dict[str, Any]) -> Effect:
    payload = {key: value for key, value in raw.items() if key != "type"}
    return Effect(type=raw["type"], payload=payload)


def _exit_from_dict(direction: str, raw: dict[str, Any]) -> ExitDefinition:
    return ExitDefinition(
        direction=direction,
        target=raw["target"],
        conditions=tuple(_condition_from_dict(item) for item in raw.get("conditions", [])),
        failure_text=raw.get("failure_text"),
    )


def _room_event_from_dict(raw: dict[str, Any]) -> RoomEventDefinition:
    return RoomEventDefinition(
        conditions=tuple(_condition_from_dict(item) for item in raw.get("conditions", [])),
        effects=tuple(_effect_from_dict(item) for item in raw.get("effects", [])),
        text=raw.get("text"),
    )


def _room_from_dict(raw: dict[str, Any]) -> RoomDefinition:
    exits = {
        direction: _exit_from_dict(direction, exit_raw)
        for direction, exit_raw in raw.get("exits", {}).items()
    }
    return RoomDefinition(
        id=raw["id"],
        zone=raw["zone"],
        name=raw["name"],
        aliases=tuple(raw.get("aliases", [])),
        first_description=raw["first_description"],
        repeat_description=raw["repeat_description"],
        exits=exits,
        objects=tuple(raw.get("objects", [])),
        scene_id=raw.get("scene"),
        tags=tuple(raw.get("tags", [])),
        context_actions=dict(raw.get("context_actions", {})),
        context_directions=dict(raw.get("context_directions", {})),
        enter_events=tuple(_room_event_from_dict(item) for item in raw.get("enter_events", [])),
    )


def _object_from_dict(raw: dict[str, Any]) -> ObjectDefinition:
    return ObjectDefinition(
        id=raw["id"],
        name=raw["name"],
        aliases=tuple(raw.get("aliases", [])),
        kind=raw["kind"],
        portable=raw["portable"],
        listed=raw.get("listed", True),
        location=raw["location"],
        description=raw["description"],
        read_text=raw.get("read_text"),
        initial_visible=raw.get("visible", True),
        initial_states=dict(raw.get("states", {})),
        on_examine_effects=tuple(
            _effect_from_dict(item) for item in raw.get("on_examine_effects", [])
        ),
        on_read_effects=tuple(
            _effect_from_dict(item) for item in raw.get("on_read_effects", [])
        ),
        on_take_effects=tuple(
            _effect_from_dict(item) for item in raw.get("on_take_effects", [])
        ),
    )


def _interaction_from_dict(raw: dict[str, Any]) -> InteractionDefinition:
    return InteractionDefinition(
        id=raw["id"],
        action=raw["action"],
        room_id=raw.get("room_id"),
        direct_object=raw.get("direct_object"),
        indirect_object=raw.get("indirect_object"),
        preposition=raw.get("preposition"),
        conditions=tuple(_condition_from_dict(item) for item in raw.get("conditions", [])),
        effects=tuple(_effect_from_dict(item) for item in raw.get("effects", [])),
        success_text=raw.get("success_text"),
        failure_text=raw.get("failure_text"),
    )


def load_game_definition(base_path: Path) -> GameDefinition:
    """Load the game definition from JSON files below *base_path*."""

    world_data = _load_json(base_path / "world.json")
    rooms_data = _load_json(base_path / "rooms.json")
    objects_data = _load_json(base_path / "objects.json")
    interactions_data = _load_json(base_path / "interactions.json")

    rooms = {room["id"]: _room_from_dict(room) for room in rooms_data}
    objects = {item["id"]: _object_from_dict(item) for item in objects_data}
    interactions = tuple(_interaction_from_dict(item) for item in interactions_data)

    definition = GameDefinition(
        title=world_data["title"],
        data_version=world_data["data_version"],
        intro=tuple(world_data.get("intro", [])),
        intro_scene=world_data.get("intro_scene"),
        start_room=world_data["start_room"],
        rooms=rooms,
        objects=objects,
        interactions=interactions,
        initial_flags=dict(world_data.get("initial_flags", {})),
    )
    validate_definition(definition)
    return definition
