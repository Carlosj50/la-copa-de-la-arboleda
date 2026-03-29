"""High-level game session runtime."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Iterable

from game.content import load_game_definition
from game.model import (
    Condition,
    Effect,
    ExitDefinition,
    GameDefinition,
    GameState,
    InteractionDefinition,
    ObjectDefinition,
    ParsedCommand,
    RoomDefinition,
)
from game.parser import parse_command
from game.persistence import SaveSystem
from game.shared.pixel_art import render_scene
from game.shared.screen import ScreenComposer, ScreenOptions
from game.shared.text import format_series, normalize_text, wrap_for_screen


DEFAULT_SAVE_NAME = "slot_001.json"
SCREEN_HINT = (
    "Escribe AYUDA si no sabes qué hacer.\n"
    "INV inventario | GUARDAR | CARGAR | FIN"
)
ZONE_LABELS = {
    "zona_1": "Bosque y alrededores",
    "zona_2": "Finca principal",
    "zona_3": "Anexos y zona oculta",
    "zona_4": "Pasadizos y cueva final",
}


class GameSession:
    """Runtime facade for the full game."""

    def __init__(
        self,
        definition: GameDefinition,
        save_system: SaveSystem,
        screen_options: ScreenOptions | None = None,
    ) -> None:
        self.definition = definition
        self.save_system = save_system
        self.screen = ScreenComposer(definition.title, screen_options)
        self.state = self._build_initial_state()
        self._screen_notice: str | None = None

    @classmethod
    def from_project_root(cls, project_root: Path) -> "GameSession":
        definition = load_game_definition(project_root / "data" / "world")
        save_system = SaveSystem(project_root / "data" / "saves" / DEFAULT_SAVE_NAME)
        return cls(definition, save_system)

    def _build_initial_state(self) -> GameState:
        object_locations = {
            object_id: definition.location
            for object_id, definition in self.definition.objects.items()
        }
        object_states = {
            object_id: {"visible": definition.initial_visible, **deepcopy(definition.initial_states)}
            for object_id, definition in self.definition.objects.items()
        }
        return GameState(
            current_room_id=self.definition.start_room,
            inventory=[],
            flags=deepcopy(self.definition.initial_flags),
            object_locations=object_locations,
            object_states=object_states,
        )

    @property
    def current_room(self) -> RoomDefinition:
        return self.definition.rooms[self.state.current_room_id]

    def intro_text(self) -> str:
        parts = [
            part
            for part in (
                self.opening_text(),
                self.render_room_screen(force_full=True),
            )
            if part
        ]
        return "\n\n".join(parts)

    def opening_text(self) -> str:
        intro_scene = render_scene(self.definition.intro_scene) if self.screen.options.show_scene else ""
        intro_blocks = "\n\n".join(self.definition.intro)
        return self.screen.compose_opening(
            scene=intro_scene,
            intro_text=intro_blocks,
            subtitle="Aventura conversacional retro",
            footer=SCREEN_HINT,
        )

    def render_room_screen(
        self,
        *,
        force_full: bool = False,
        result: str | None = None,
    ) -> str:
        room = self.current_room
        title, description, detail_lines = self._room_view(force_full=force_full)
        return self.screen.compose_room(
            scene=self._scene_for_room(room),
            room_title=title,
            room_subtitle=ZONE_LABELS.get(room.zone),
            description=description,
            detail_lines=detail_lines,
            result=result,
            footer=SCREEN_HINT,
        )

    def render_special_screen(self, title: str, body: str) -> str:
        return self.screen.compose_message(
            scene=self._scene_for_room(self.current_room),
            title=title,
            subtitle=ZONE_LABELS.get(self.current_room.zone),
            body=body,
            footer=SCREEN_HINT,
        )

    def execute(self, raw_text: str, as_screen: bool = False) -> str:
        self._screen_notice = None
        command = parse_command(raw_text)
        if command.is_error:
            response = command.error_message or "No entiendo."
            return self.render_room_screen(result=response) if as_screen else response

        previous_room_id = self.state.current_room_id
        response = self._dispatch(command)
        if not as_screen:
            return response
        return self._render_screen_response(command, response, previous_room_id)

    def describe_current_room(self, force_full: bool = False) -> str:
        room = self.current_room
        title, description, detail_lines = self._room_view(force_full=force_full)
        parts = [part for part in (self._scene_for_room(room), wrap_for_screen(title), wrap_for_screen(description)) if part]
        parts.extend(wrap_for_screen(line) for line in detail_lines)
        return "\n".join(parts)

    def _room_view(self, force_full: bool = False) -> tuple[str, str, list[str]]:
        room = self.current_room
        first_time = room.id not in self.state.visited_rooms
        description = room.first_description if (force_full or first_time) else room.repeat_description
        self.state.visited_rooms.add(room.id)
        return room.name, description, self._room_summary_lines()

    def _room_summary_lines(self) -> list[str]:
        visible_names = [
            self.definition.objects[object_id].name
            for object_id in self._visible_room_object_ids()
            if self.definition.objects[object_id].listed
        ]
        exits = [direction.lower() for direction in self._available_exit_directions()]

        parts: list[str] = []
        if visible_names:
            parts.append(f"Ves aquí {format_series(visible_names)}.")
        if exits:
            parts.append(f"Salidas: {', '.join(exits)}.")
        else:
            parts.append("No ves una salida clara.")
        return parts

    def _scene_for_room(self, room: RoomDefinition) -> str:
        if not self.screen.options.show_scene:
            return ""

        scene_id = room.scene_id
        if scene_id is None:
            if room.zone == "zona_1":
                scene_id = "exterior_generico"
            elif room.zone == "zona_2":
                scene_id = "interior_generico"
            elif room.zone == "zona_3":
                scene_id = "anexo_generico"
            else:
                scene_id = "subterraneo_generico"
        return render_scene(scene_id)

    def _render_screen_response(
        self,
        command: ParsedCommand,
        response: str,
        previous_room_id: str,
    ) -> str:
        if self.state.exit_requested:
            return self.render_special_screen("Fin de la sesión", response)
        if self.state.game_over:
            return self.render_special_screen("La Copa de la Arboleda", response)
        if command.action == "MIRAR":
            return self.render_room_screen(force_full=False)
        if command.action == "EXAMINAR" and (
            command.direct_text is None or self._match_current_room(command.direct_text)
        ):
            return self.render_room_screen(force_full=True)
        if command.action == "CARGAR" and response.startswith("Partida cargada."):
            return self.render_room_screen(force_full=False, result=self._screen_notice or "Partida cargada.")
        if command.action in {"IR", "ENTRAR", "SALIR"} and self.state.current_room_id != previous_room_id:
            return self.render_room_screen(force_full=False, result=self._screen_notice)
        return self.render_room_screen(force_full=False, result=response)

    def _dispatch(self, command: ParsedCommand) -> str:
        action = command.action
        if action == "FIN":
            self.state.exit_requested = True
            return "Cierras la carpeta de notas y dejas La Arboleda por hoy."
        if action == "AYUDA":
            return self._help_text()
        if action == "INVENTARIO":
            return self._inventory_text()
        if action == "GUARDAR":
            self.save_system.save(self.definition, self.state)
            return "Partida guardada en data/saves/slot_001.json."
        if action == "CARGAR":
            if not self.save_system.exists():
                return "Aún no hay ninguna partida guardada."
            self.state = self.save_system.load(self.definition)
            self._screen_notice = "Partida cargada."
            return "Partida cargada."
        if action == "MIRAR":
            return self.describe_current_room(force_full=False)
        if action in {"IR"}:
            if command.direction is None:
                return "No queda claro hacia dónde quieres ir."
            return self._move(command.direction)
        if action in {"ENTRAR", "SALIR"}:
            return self._contextual_move(action)
        if action == "EXAMINAR":
            if command.direct_text is None:
                return self.describe_current_room(force_full=False)
            return self._examine(command.direct_text)
        if action == "LEER":
            if command.direct_text is None:
                return "No hay nada legible así."
            return self._read(command.direct_text)
        if action == "COGER":
            if command.direct_text is None:
                return "No queda claro qué quieres coger."
            return self._take(command.direct_text)
        if action == "SOLTAR":
            if command.direct_text is None:
                return "No queda claro qué quieres soltar."
            return self._drop(command.direct_text)
        if action in {"ENCENDER", "APAGAR"}:
            if command.direct_text is None:
                return "Te falta concretar qué quieres encender o apagar."
            return self._toggle_light(action, command.direct_text)
        if action in {"USAR", "ABRIR", "CERRAR", "EMPUJAR", "TIRAR"}:
            return self._run_interaction(command)
        return "Ahora mismo eso no sirve."

    def _help_text(self) -> str:
        return (
            "Comandos base: MIRAR, EXAMINAR, IR, NORTE, SUR, ESTE, OESTE, ARRIBA, ABAJO, "
            "COGER, SOLTAR, ABRIR, CERRAR, USAR, EMPUJAR, TIRAR, LEER, ENCENDER, APAGAR, "
            "INVENTARIO, AYUDA, GUARDAR, CARGAR y FIN.\n"
            "Alias útiles: MIRA, VER, COGE, RECOGE, PONER, USA, INV, I.\n"
            "Formas útiles: VERBO, DIRECCIÓN, VERBO OBJETO, VERBO OBJETO EN OBJETO. "
            "ENTRAR y SALIR funcionan cuando la salida contextual es obvia."
        )

    def _inventory_text(self) -> str:
        if not self.state.inventory:
            return "No llevas nada."
        items = [self.definition.objects[item_id].name for item_id in self.state.inventory]
        return f"Llevas {format_series(items)}."

    def _available_exit_directions(self) -> list[str]:
        available = []
        for direction, exit_definition in self.current_room.exits.items():
            if self._conditions_met(exit_definition.conditions):
                available.append(direction)
        return available

    def _move(self, direction: str) -> str:
        direction = self.current_room.context_directions.get(direction, direction)
        exit_definition = self.current_room.exits.get(direction)
        if exit_definition is None:
            return "Por ahí no puedes pasar."
        if not self._conditions_met(exit_definition.conditions):
            return exit_definition.failure_text or "Por ahí no puedes pasar."

        self.state.current_room_id = exit_definition.target
        event_texts = self._apply_room_enter_events()
        self._screen_notice = event_texts or None
        room_text = self.describe_current_room(force_full=False)
        if event_texts:
            return f"{event_texts}\n\n{room_text}"
        return room_text

    def _contextual_move(self, action: str) -> str:
        mapped_direction = self.current_room.context_actions.get(action)
        if mapped_direction is None:
            if action == "ENTRAR":
                return "Desde aquí no queda claro por dónde entrar."
            return "Desde aquí no queda claro por dónde salir."
        return self._move(mapped_direction)

    def _examine(self, raw_target: str) -> str:
        room_match = self._match_current_room(raw_target)
        if room_match:
            return self.describe_current_room(force_full=True)

        object_id, error = self._resolve_object(raw_target)
        if object_id is None:
            return error

        definition = self.definition.objects[object_id]
        self._apply_effects(definition.on_examine_effects)
        return definition.description

    def _read(self, raw_target: str) -> str:
        object_id, error = self._resolve_object(raw_target)
        if object_id is None:
            return error

        definition = self.definition.objects[object_id]
        if not definition.read_text:
            return "No hay nada legible ahí."
        self._apply_effects(definition.on_read_effects)
        return definition.read_text

    def _take(self, raw_target: str) -> str:
        object_id, error = self._resolve_object(raw_target, inventory_scope=False)
        if object_id is None:
            return error

        definition = self.definition.objects[object_id]
        if not self._object_is_visible(object_id):
            return "No ves eso aquí."
        if self.state.object_locations[object_id] != self.state.current_room_id:
            return "No ves eso aquí."
        if not definition.portable or self._object_state(object_id, "fixed", False):
            return "No puedes coger eso."
        if object_id in self.state.inventory:
            return "Ya lo llevas contigo."

        self.state.inventory.append(object_id)
        self.state.object_locations[object_id] = "__inventory__"
        self._apply_effects(definition.on_take_effects)
        return f"Coges {definition.name}."

    def _drop(self, raw_target: str) -> str:
        object_id, error = self._resolve_inventory_object(raw_target)
        if object_id is None:
            return error

        definition = self.definition.objects[object_id]
        self.state.inventory.remove(object_id)
        self.state.object_locations[object_id] = self.state.current_room_id
        self.state.object_states[object_id]["visible"] = True
        return f"Dejas {definition.name}."

    def _toggle_light(self, action: str, raw_target: str) -> str:
        object_id, error = self._resolve_inventory_object(raw_target)
        if object_id is None:
            return error
        if object_id != "lampara_aceite":
            return "Ahora mismo eso no sirve."

        state = self.state.object_states[object_id]
        if action == "ENCENDER":
            if state.get("lit"):
                return "La lámpara ya está encendida."
            if not state.get("filled"):
                return "La lámpara sigue seca."
            if "caja_cerillas" not in self.state.inventory:
                return "Necesitas algo con que prenderla."
            state["lit"] = True
            self.state.flags["lamp_lit"] = True
            return "La llama prende con una luz baja pero estable."

        if not state.get("lit"):
            return "La lámpara ya está apagada."
        state["lit"] = False
        self.state.flags["lamp_lit"] = False
        return "Apagas la lámpara."

    def _run_interaction(self, command: ParsedCommand) -> str:
        direct_id = None
        indirect_id = None

        if command.direct_text:
            direct_id, error = self._resolve_object(command.direct_text)
            if direct_id is None:
                return error
        if command.indirect_text:
            indirect_id, error = self._resolve_object(command.indirect_text)
            if indirect_id is None:
                return error

        interaction = self._find_interaction(command.action, direct_id, indirect_id, command.preposition)
        swapped = False
        if interaction is None and command.action == "USAR" and direct_id and indirect_id:
            interaction = self._find_interaction(
                command.action,
                indirect_id,
                direct_id,
                command.preposition,
            )
            swapped = interaction is not None

        if interaction is None:
            return "Ahora mismo eso no sirve."

        if not self._conditions_met(interaction.conditions):
            return interaction.failure_text or "Así no consigues nada."

        self._apply_effects(interaction.effects)
        if self.state.game_over:
            return self._build_ending_text()
        if interaction.success_text:
            return interaction.success_text
        if swapped:
            return "Funciona, aunque el gesto no era exactamente ese."
        return "Hecho."

    def _find_interaction(
        self,
        action: str,
        direct_id: str | None,
        indirect_id: str | None,
        preposition: str | None,
    ) -> InteractionDefinition | None:
        candidates: list[tuple[int, InteractionDefinition]] = []
        for interaction in self.definition.interactions:
            if interaction.action != action:
                continue
            if interaction.room_id and interaction.room_id != self.state.current_room_id:
                continue
            if interaction.direct_object != direct_id:
                continue
            if interaction.indirect_object != indirect_id:
                continue
            if interaction.preposition and interaction.preposition != preposition:
                continue
            score = 0
            if interaction.room_id:
                score += 4
            if interaction.direct_object:
                score += 2
            if interaction.indirect_object:
                score += 2
            if interaction.preposition:
                score += 1
            candidates.append((score, interaction))

        if not candidates:
            return None
        candidates.sort(key=lambda item: item[0], reverse=True)
        return candidates[0][1]

    def _match_current_room(self, raw_target: str) -> bool:
        normalized = normalize_text(raw_target)
        if normalized == normalize_text(self.current_room.name):
            return True
        return any(normalized == normalize_text(alias) for alias in self.current_room.aliases)

    def _resolve_object(
        self,
        raw_target: str,
        inventory_scope: bool = True,
    ) -> tuple[str | None, str]:
        normalized = normalize_text(raw_target)
        matches: list[str] = []
        for object_id in self._candidate_object_ids(inventory_scope=inventory_scope):
            definition = self.definition.objects[object_id]
            names = [definition.name, *definition.aliases]
            if any(normalized == normalize_text(name) for name in names):
                matches.append(object_id)

        unique_matches = list(dict.fromkeys(matches))
        if not unique_matches:
            return None, "No ves eso aquí."
        if len(unique_matches) > 1:
            return None, "Hay más de una cosa que podría encajar. Sé más concreto."
        return unique_matches[0], ""

    def _resolve_inventory_object(self, raw_target: str) -> tuple[str | None, str]:
        normalized = normalize_text(raw_target)
        matches: list[str] = []
        for object_id in self.state.inventory:
            definition = self.definition.objects[object_id]
            names = [definition.name, *definition.aliases]
            if any(normalized == normalize_text(name) for name in names):
                matches.append(object_id)
        unique_matches = list(dict.fromkeys(matches))
        if not unique_matches:
            return None, "No llevas eso contigo."
        if len(unique_matches) > 1:
            return None, "Hay más de una cosa que podría encajar. Sé más concreto."
        return unique_matches[0], ""

    def _candidate_object_ids(self, inventory_scope: bool = True) -> Iterable[str]:
        room_objects = self._visible_room_object_ids()
        if inventory_scope:
            return [*room_objects, *self.state.inventory]
        return room_objects

    def _visible_room_object_ids(self) -> list[str]:
        return [
            object_id
            for object_id, location in self.state.object_locations.items()
            if location == self.state.current_room_id and self._object_is_visible(object_id)
        ]

    def _object_is_visible(self, object_id: str) -> bool:
        return bool(self.state.object_states[object_id].get("visible", True))

    def _object_state(self, object_id: str, key: str, default: object | None = None) -> object:
        return self.state.object_states[object_id].get(key, default)

    def _conditions_met(self, conditions: tuple[Condition, ...]) -> bool:
        return all(self._condition_met(condition) for condition in conditions)

    def _condition_met(self, condition: Condition) -> bool:
        payload = condition.payload
        kind = condition.type
        if kind == "flag_true":
            return bool(self.state.flags.get(payload["name"], False))
        if kind == "flag_false":
            return not bool(self.state.flags.get(payload["name"], False))
        if kind == "inventory_contains":
            return payload["object_id"] in self.state.inventory
        if kind == "inventory_not_contains":
            return payload["object_id"] not in self.state.inventory
        if kind == "object_state_is":
            return self.state.object_states[payload["object_id"]].get(payload["state"]) == payload["value"]
        if kind == "object_in_room":
            return self.state.object_locations[payload["object_id"]] == self.state.current_room_id
        if kind == "current_room_is":
            return self.state.current_room_id == payload["room_id"]
        return False

    def _apply_room_enter_events(self) -> str:
        messages: list[str] = []
        for event in self.current_room.enter_events:
            if self._conditions_met(event.conditions):
                self._apply_effects(event.effects)
                if event.text:
                    messages.append(event.text)
        return "\n".join(messages)

    def _apply_effects(self, effects: tuple[Effect, ...]) -> None:
        for effect in effects:
            payload = effect.payload
            kind = effect.type
            if kind == "set_flag":
                self.state.flags[payload["name"]] = payload["value"]
            elif kind == "set_object_state":
                self.state.object_states[payload["object_id"]][payload["state"]] = payload["value"]
            elif kind == "move_object":
                self.state.object_locations[payload["object_id"]] = payload["location"]
                if payload["location"] != "__inventory__" and payload["object_id"] in self.state.inventory:
                    self.state.inventory.remove(payload["object_id"])
                if payload["location"] == "__inventory__" and payload["object_id"] not in self.state.inventory:
                    self.state.inventory.append(payload["object_id"])
            elif kind == "end_game":
                self.state.game_over = True
            elif kind == "reveal_object":
                self.state.object_states[payload["object_id"]]["visible"] = True
            else:
                raise ValueError(f"Unsupported effect type: {kind}")

    def _build_ending_text(self) -> str:
        comprehension_flags = [
            self.state.flags.get("portrait_clue_found", False),
            self.state.flags.get("library_history_found", False),
            self.state.flags.get("bedroom_letter_found", False),
        ]
        rich_ending = sum(1 for value in comprehension_flags if value) >= 2
        if rich_ending:
            return (
                "La copa encaja en el pedestal con una docilidad casi triste. La caja cede y dentro "
                "esperan la escritura de Adela, el registro de las familias y la nota final de Salvador.\n\n"
                "Los nombres terminan de ordenar la cadena que sostuvo el secreto: Adela confió en "
                "Inocencio, Inocencio lo pasó a Elvira y Salvador llegó a custodiar lo que nunca debió "
                "volverse botín.\n\n"
                "\"No te lo dejo para que poseas nada. Te lo dejo para que entiendas por qué lo guardé. "
                "Nos tocó custodiar, no apropiarnos.\" \n\n"
                "Ahora sabes que La Arboleda nunca escondió un tesoro, sino una promesa. Y sabes también "
                "por qué Salvador pensó en ti: porque fuiste de los pocos que escucharon sin reírse del lugar.\n\n"
                "Has alcanzado el final con comprensión plena."
            )
        return (
            "La copa vuelve a su sitio y la caja de documentos se abre. Entre papeles resecos y firmas antiguas "
            "entiendes lo esencial: bajo la finca se ocultaba una cesión y una deuda moral, no una fortuna.\n\n"
            "La Arboleda te entrega una verdad sobria y pesada. Ya no buscas una herencia; ahora sabes que "
            "te han confiado una memoria.\n\n"
            "Has alcanzado el final principal."
        )
