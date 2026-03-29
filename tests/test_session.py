from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from game.content import load_game_definition
from game.engine import GameSession
from game.persistence import SaveSystem
from game.shared.screen import build_compass_lines, center_block, visible_width


def build_session(tmp_dir: str) -> GameSession:
    definition = load_game_definition(PROJECT_ROOT / "data" / "world")
    save_system = SaveSystem(Path(tmp_dir) / "slot_001.json")
    return GameSession(definition, save_system)


def run_commands(session: GameSession, commands: list[str]) -> str:
    response = ""
    for command in commands:
        response = session.execute(command)
    return response


class SessionTests(unittest.TestCase):
    def _strip_ansi(self, text: str) -> str:
        return re.sub(r"\x1b\[[0-9;]*m", "", text)

    def test_opening_text_includes_help_hint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = session.opening_text()
            self.assertIn("Escribe AYUDA si no sabes qué hacer.", response)
            self.assertIn("Aventura conversacional retro", response)

    def test_compass_lines_render_fixed_rose(self) -> None:
        self.assertEqual(
            [self._strip_ansi(line) for line in build_compass_lines()],
            ["    N    ", "   /|\\   ", " O--+--E ", "   \\|/   ", "    S    "],
        )

    def test_screen_text_is_wrapped_to_fixed_width(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = session.render_room_screen(force_full=True)
            line_widths = [visible_width(line) for line in response.splitlines() if line]
            self.assertGreaterEqual(len(line_widths), 10)
            self.assertTrue(
                all(width <= session.screen.options.frame_width for width in line_widths),
                msg=response,
            )

    def test_center_block_applies_horizontal_and_vertical_padding(self) -> None:
        block = "┌──┐\n│OK│\n└──┘"
        response = center_block(block, terminal_width=20, terminal_height=9, reserve_lines=0)
        lines = response.splitlines()
        non_empty = [line for line in lines if line]
        self.assertEqual(lines[:3], ["", "", ""])
        self.assertTrue(all(line.startswith(" " * 8) for line in non_empty))

    def test_inventory_screen_mode_rebuilds_full_room_screen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = session.execute("inventario", as_screen=True)
            self.assertIn("Camino de entrada", response)
            self.assertIn("Bosque y alrededores", response)
            self.assertIn("[ RESULTADO ]", response)
            self.assertIn("No llevas nada.", response)
            self.assertIn("Salidas: este.", response)
            self.assertIn("Escribe AYUDA si no sabes qué hacer.", response)

    def test_invalid_move_screen_mode_keeps_room_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = session.execute("norte", as_screen=True)
            self.assertIn("Camino de entrada", response)
            self.assertIn("[ RESULTADO ]", response)
            self.assertIn("Por ahí no puedes pasar.", response)

    def test_usar_sin_objeto_da_mensaje_claro(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = session.execute("usar")
            self.assertEqual(response, "No queda claro qué quieres usar.")

    def test_usar_sin_objeto_indirecto_pide_mas_precision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = session.execute("usar llave")
            self.assertEqual(response, "Te falta concretar dónde o en qué quieres usar eso.")

    def test_abrir_sin_objeto_da_mensaje_claro(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = session.execute("abrir")
            self.assertEqual(response, "No queda claro qué quieres abrir.")

    def test_cerrar_objeto_no_cerrable_da_mensaje_especifico(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            session.execute("este")
            session.execute("norte")
            response = session.execute("cerrar pozo")
            self.assertEqual(response, "Eso no parece algo que puedas cerrar.")

    def test_empujar_objeto_sin_uso_da_mensaje_especifico(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            session.execute("este")
            session.execute("norte")
            response = session.execute("empujar pozo")
            self.assertEqual(response, "Empujarlo no cambia nada.")

    def test_intro_text_includes_pixel_splash_and_room_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = session.intro_text()
            self.assertIn("\x1b[", response)
            self.assertIn("Camino de entrada", response)

    def test_first_move_keeps_scene_and_room_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = session.execute("este", as_screen=True)
            self.assertIn("\x1b[", response)
            self.assertIn("Cruce del bosque", response)

    def test_room_screen_includes_compass_in_upper_right_scene_area(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = self._strip_ansi(session.render_room_screen(force_full=True))
            self.assertIn("O--+--E", response)
            scene_rows = [line for line in response.splitlines() if line.startswith("│")]
            compass_row = next(line for line in scene_rows if "O--+--E" in line)
            self.assertTrue(compass_row.endswith("O--+--E   │"), msg=compass_row)

    def test_examinar_fixture_no_choca_con_alias_de_habitacion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            session.execute("este")
            session.execute("norte")
            response = session.execute("examinar pozo")
            self.assertIn("brocal", response)

    def test_contextual_entrar_en_patio_exterior(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            commands = [
                "este",
                "norte",
                "coger tabla",
                "este",
                "usar tabla en zanja",
                "este",
                "norte",
                "norte",
                "oeste",
                "sur",
                "oeste",
            ]
            run_commands(session, commands)
            response = session.execute("entrar", as_screen=True)
            self.assertIn("Vestíbulo", response)

    def test_contextual_salir_en_dormitorio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            commands = [
                "este",
                "norte",
                "coger tabla",
                "este",
                "usar tabla en zanja",
                "este",
                "norte",
                "norte",
                "oeste",
                "sur",
                "este",
                "norte",
            ]
            run_commands(session, commands)
            response = session.execute("salir", as_screen=True)
            self.assertIn("Biblioteca", response)

    def test_salir_sin_contexto_da_respuesta_clara(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = session.execute("salir")
            self.assertEqual(response, "Desde aquí no queda claro por dónde salir.")

    def test_poner_como_alias_de_usar_funciona_en_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            commands = [
                "este",
                "norte",
                "coger tabla",
                "este",
                "usar tabla en zanja",
                "este",
                "norte",
                "coger cerillas",
                "coger llave",
                "norte",
                "oeste",
                "sur",
                "este",
                "norte",
                "coger lampara",
                "sur",
                "oeste",
                "oeste",
                "usar llave en puerta",
                "sur",
                "norte",
                "este",
                "norte",
                "este",
                "sur",
                "sur",
                "este",
                "este",
                "coger aceite",
            ]
            run_commands(session, commands)
            response = session.execute("poner aceite en lampara")
            self.assertIn("Rellenas la lámpara", response)

    def test_save_and_load_restore_progress(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            session.execute("este")
            session.execute("norte")
            session.execute("coger tabla")
            save_response = session.execute("guardar")
            self.assertIn("Partida guardada", save_response)

            session.execute("este")
            self.assertEqual(session.state.current_room_id, "valla_rota")

            load_response = session.execute("cargar", as_screen=True)
            self.assertIn("Partida cargada", load_response)
            self.assertIn("[ RESULTADO ]", load_response)
            self.assertEqual(session.state.current_room_id, "claro_pozo_seco")
            self.assertIn("tabla_suelta", session.state.inventory)

    def test_main_ending_walkthrough(self) -> None:
        commands = [
            "este",
            "norte",
            "coger tabla",
            "este",
            "usar tabla en zanja",
            "este",
            "norte",
            "coger cerillas",
            "coger llave",
            "norte",
            "oeste",
            "sur",
            "este",
            "coger vidriera",
            "norte",
            "coger lampara",
            "coger cuaderno",
            "sur",
            "oeste",
            "oeste",
            "usar llave en puerta",
            "sur",
            "coger cuerda",
            "coger pala",
            "coger gancho",
            "norte",
            "este",
            "norte",
            "este",
            "sur",
            "sur",
            "este",
            "coger vara",
            "este",
            "coger aceite",
            "usar pala en bancal",
            "coger medallon",
            "usar aceite en lampara",
            "oeste",
            "oeste",
            "sur",
            "usar vidriera en roseton",
            "usar medallon en altar",
            "coger copa",
            "este",
            "coger placa",
            "usar vara en losa",
            "abajo",
            "encender lampara",
            "este",
            "este",
            "usar gancho en anillas",
            "usar copa en agua",
            "este",
            "usar placa en hendidura",
            "usar copa en cuenco",
            "este",
            "usar copa en pedestal",
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = run_commands(session, commands)
            self.assertTrue(session.state.game_over)
            self.assertIn("final principal", response)

    def test_rich_ending_walkthrough(self) -> None:
        commands = [
            "este",
            "norte",
            "coger tabla",
            "este",
            "usar tabla en zanja",
            "este",
            "norte",
            "coger cerillas",
            "coger llave",
            "norte",
            "oeste",
            "sur",
            "examinar retrato",
            "este",
            "leer legajos",
            "coger vidriera",
            "norte",
            "coger lampara",
            "coger cuaderno",
            "sur",
            "oeste",
            "oeste",
            "usar llave en puerta",
            "sur",
            "coger cuerda",
            "coger pala",
            "coger gancho",
            "norte",
            "este",
            "norte",
            "este",
            "sur",
            "sur",
            "este",
            "coger vara",
            "este",
            "coger aceite",
            "usar pala en bancal",
            "coger medallon",
            "usar aceite en lampara",
            "oeste",
            "oeste",
            "norte",
            "norte",
            "oeste",
            "sur",
            "este",
            "norte",
            "abrir cajon",
            "leer carta",
            "sur",
            "oeste",
            "norte",
            "este",
            "sur",
            "sur",
            "sur",
            "usar vidriera en roseton",
            "usar medallon en altar",
            "coger copa",
            "este",
            "coger placa",
            "usar vara en losa",
            "abajo",
            "encender lampara",
            "este",
            "este",
            "usar gancho en anillas",
            "usar copa en agua",
            "este",
            "usar placa en hendidura",
            "usar copa en cuenco",
            "este",
            "usar copa en pedestal",
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = build_session(tmp_dir)
            response = run_commands(session, commands)
            self.assertTrue(session.state.game_over)
            self.assertIn("comprensión plena", response)


if __name__ == "__main__":
    unittest.main()
