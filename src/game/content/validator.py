"""Validation helpers for authored content."""

from __future__ import annotations

from game.model import Condition, Effect, GameDefinition, RoomDefinition
from game.shared.pixel_art import has_scene
from game.shared.text import normalize_text


SUPPORTED_OBJECT_KINDS = {"main", "optional", "ambient", "fixture"}
SUPPORTED_PREPOSITIONS = {"EN", "CON", "A"}
SUPPORTED_CONDITIONS = {
    "flag_true",
    "flag_false",
    "inventory_contains",
    "inventory_not_contains",
    "object_state_is",
    "object_in_room",
    "current_room_is",
}
SUPPORTED_EFFECTS = {
    "set_flag",
    "set_object_state",
    "move_object",
    "end_game",
    "reveal_object",
}


def _require_keys(payload: dict[str, object], keys: tuple[str, ...], owner: str, kind: str) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        raise ValueError(f"{owner} uses {kind} without keys: {', '.join(missing)}")


def _require_flag(definition: GameDefinition, flag_name: str, owner: str, kind: str) -> None:
    if flag_name not in definition.initial_flags:
        raise ValueError(f"{owner} uses unknown flag {flag_name} in {kind}")


def _require_object(definition: GameDefinition, object_id: str, owner: str, kind: str) -> None:
    if object_id not in definition.objects:
        raise ValueError(f"{owner} uses unknown object {object_id} in {kind}")


def _require_room(definition: GameDefinition, room_id: str, owner: str, kind: str) -> None:
    if room_id not in definition.rooms:
        raise ValueError(f"{owner} uses unknown room {room_id} in {kind}")


def _validate_condition(definition: GameDefinition, condition: Condition, owner: str) -> None:
    payload = condition.payload
    kind = condition.type
    if kind not in SUPPORTED_CONDITIONS:
        raise ValueError(f"{owner} uses unsupported condition type {kind}")

    if kind in {"flag_true", "flag_false"}:
        _require_keys(payload, ("name",), owner, kind)
        _require_flag(definition, str(payload["name"]), owner, kind)
        return

    if kind in {"inventory_contains", "inventory_not_contains", "object_in_room"}:
        _require_keys(payload, ("object_id",), owner, kind)
        _require_object(definition, str(payload["object_id"]), owner, kind)
        return

    if kind == "object_state_is":
        _require_keys(payload, ("object_id", "state", "value"), owner, kind)
        _require_object(definition, str(payload["object_id"]), owner, kind)
        return

    if kind == "current_room_is":
        _require_keys(payload, ("room_id",), owner, kind)
        _require_room(definition, str(payload["room_id"]), owner, kind)


def _validate_effect(definition: GameDefinition, effect: Effect, owner: str) -> None:
    payload = effect.payload
    kind = effect.type
    if kind not in SUPPORTED_EFFECTS:
        raise ValueError(f"{owner} uses unsupported effect type {kind}")

    if kind == "set_flag":
        _require_keys(payload, ("name", "value"), owner, kind)
        _require_flag(definition, str(payload["name"]), owner, kind)
        return

    if kind == "set_object_state":
        _require_keys(payload, ("object_id", "state", "value"), owner, kind)
        _require_object(definition, str(payload["object_id"]), owner, kind)
        return

    if kind == "move_object":
        _require_keys(payload, ("object_id", "location"), owner, kind)
        _require_object(definition, str(payload["object_id"]), owner, kind)
        location = str(payload["location"])
        if location not in definition.rooms and location not in {"__inventory__", "__nowhere__"}:
            raise ValueError(f"{owner} uses unknown location {location} in {kind}")
        return

    if kind == "reveal_object":
        _require_keys(payload, ("object_id",), owner, kind)
        _require_object(definition, str(payload["object_id"]), owner, kind)


def _validate_room_aliases(definition: GameDefinition, room: RoomDefinition) -> None:
    room_tokens = {
        normalize_text(room.name),
        *(normalize_text(alias) for alias in room.aliases),
    }
    object_tokens: dict[str, set[str]] = {}
    for object_id in room.objects:
        definition_object = definition.objects[object_id]
        for candidate in (definition_object.name, *definition_object.aliases):
            token = normalize_text(candidate)
            object_tokens.setdefault(token, set()).add(object_id)

    collisions = sorted(token for token in room_tokens if token and token in object_tokens)
    if collisions:
        raise ValueError(
            f"Room {room.id} has aliases colliding with local objects: {', '.join(collisions)}"
        )

    duplicated = {
        token: sorted(object_ids)
        for token, object_ids in object_tokens.items()
        if token and len(object_ids) > 1
    }
    if duplicated:
        duplicated_text = ", ".join(
            f"{token} -> {', '.join(object_ids)}" for token, object_ids in duplicated.items()
        )
        raise ValueError(f"Room {room.id} has duplicated local aliases: {duplicated_text}")


def validate_definition(definition: GameDefinition) -> None:
    """Raise ValueError if the authored definition is inconsistent."""

    if definition.start_room not in definition.rooms:
        raise ValueError(f"Unknown start room: {definition.start_room}")
    if not has_scene(definition.intro_scene):
        raise ValueError(f"Unknown intro scene: {definition.intro_scene}")

    for room in definition.rooms.values():
        if not has_scene(room.scene_id):
            raise ValueError(f"Room {room.id} uses unknown scene {room.scene_id}")
        for exit_definition in room.exits.values():
            if exit_definition.target not in definition.rooms:
                raise ValueError(
                    f"Room {room.id} points to unknown room {exit_definition.target}"
                )
            for condition in exit_definition.conditions:
                _validate_condition(
                    definition,
                    condition,
                    f"Room exit {room.id}:{exit_definition.direction}",
                )

        for object_id in room.objects:
            if object_id not in definition.objects:
                raise ValueError(f"Room {room.id} references unknown object {object_id}")
            if definition.objects[object_id].location != room.id:
                raise ValueError(
                    f"Room {room.id} lists object {object_id} but its location is "
                    f"{definition.objects[object_id].location}"
                )

        for action, direction in room.context_actions.items():
            if direction not in room.exits:
                raise ValueError(
                    f"Room {room.id} maps context action {action} to unknown exit {direction}"
                )

        for direction_alias, direction in room.context_directions.items():
            if direction not in room.exits:
                raise ValueError(
                    f"Room {room.id} maps context direction {direction_alias} to unknown exit {direction}"
                )

        for index, event in enumerate(room.enter_events, start=1):
            owner = f"Room event {room.id}#{index}"
            for condition in event.conditions:
                _validate_condition(definition, condition, owner)
            for effect in event.effects:
                _validate_effect(definition, effect, owner)

        _validate_room_aliases(definition, room)

    for object_definition in definition.objects.values():
        location = object_definition.location
        if location not in definition.rooms and location != "__nowhere__":
            raise ValueError(
                f"Object {object_definition.id} has unknown location {location}"
            )
        if object_definition.kind not in SUPPORTED_OBJECT_KINDS:
            raise ValueError(
                f"Object {object_definition.id} uses unsupported kind {object_definition.kind}"
            )
        for effect in object_definition.on_examine_effects:
            _validate_effect(definition, effect, f"Object {object_definition.id} on_examine")
        for effect in object_definition.on_read_effects:
            _validate_effect(definition, effect, f"Object {object_definition.id} on_read")
        for effect in object_definition.on_take_effects:
            _validate_effect(definition, effect, f"Object {object_definition.id} on_take")

    for interaction in definition.interactions:
        if interaction.room_id and interaction.room_id not in definition.rooms:
            raise ValueError(
                f"Interaction {interaction.id} points to unknown room {interaction.room_id}"
            )
        for object_key in (interaction.direct_object, interaction.indirect_object):
            if object_key and object_key not in definition.objects:
                raise ValueError(
                    f"Interaction {interaction.id} points to unknown object {object_key}"
                )
        if interaction.preposition and interaction.preposition not in SUPPORTED_PREPOSITIONS:
            raise ValueError(
                f"Interaction {interaction.id} uses unsupported preposition {interaction.preposition}"
            )
        for condition in interaction.conditions:
            _validate_condition(definition, condition, f"Interaction {interaction.id}")
        for effect in interaction.effects:
            _validate_effect(definition, effect, f"Interaction {interaction.id}")
