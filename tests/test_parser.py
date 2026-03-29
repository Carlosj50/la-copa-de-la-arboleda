from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from game.parser import parse_command


class ParserTests(unittest.TestCase):
    def test_entrada_vacia_devuelve_error(self) -> None:
        command = parse_command("   ")
        self.assertTrue(command.is_error)
        self.assertEqual(command.error_message, "No has escrito ningún comando.")

    def test_alias_mirar(self) -> None:
        command = parse_command("que ves?")
        self.assertEqual(command.action, "MIRAR")
        self.assertFalse(command.is_error)

    def test_alias_imperativo_mira_funciona(self) -> None:
        command = parse_command("mira")
        self.assertEqual(command.action, "MIRAR")
        self.assertFalse(command.is_error)

    def test_ver_con_objeto_se_vuelve_examinar(self) -> None:
        command = parse_command("ver cuaderno")
        self.assertEqual(command.action, "EXAMINAR")
        self.assertEqual(command.direct_text, "CUADERNO")

    def test_direccion_simple(self) -> None:
        command = parse_command("n")
        self.assertEqual(command.action, "IR")
        self.assertEqual(command.direction, "NORTE")

    def test_alias_poner_se_vuelve_usar(self) -> None:
        command = parse_command("poner aceite en lampara")
        self.assertEqual(command.action, "USAR")
        self.assertEqual(command.direct_text, "ACEITE")
        self.assertEqual(command.indirect_text, "LAMPARA")

    def test_alias_coge_se_vuelve_coger(self) -> None:
        command = parse_command("coge cuerda")
        self.assertEqual(command.action, "COGER")
        self.assertEqual(command.direct_text, "CUERDA")

    def test_alias_recoge_se_vuelve_coger(self) -> None:
        command = parse_command("recoge pala")
        self.assertEqual(command.action, "COGER")
        self.assertEqual(command.direct_text, "PALA")

    def test_alias_usa_se_vuelve_usar(self) -> None:
        command = parse_command("usa llave en puerta")
        self.assertEqual(command.action, "USAR")
        self.assertEqual(command.direct_text, "LLAVE")
        self.assertEqual(command.indirect_text, "PUERTA")

    def test_articulos_y_al_se_normalizan(self) -> None:
        command = parse_command("usar la copa al cuenco")
        self.assertEqual(command.action, "USAR")
        self.assertEqual(command.direct_text, "COPA")
        self.assertEqual(command.indirect_text, "CUENCO")
        self.assertEqual(command.preposition, "A")

    def test_comando_con_tildes_se_normaliza(self) -> None:
        command = parse_command("poner aceite en lámpara")
        self.assertEqual(command.action, "USAR")
        self.assertEqual(command.direct_text, "ACEITE")
        self.assertEqual(command.indirect_text, "LAMPARA")

    def test_forma_con_objeto_indirecto(self) -> None:
        command = parse_command("usar llave en puerta")
        self.assertEqual(command.action, "USAR")
        self.assertEqual(command.direct_text, "LLAVE")
        self.assertEqual(command.indirect_text, "PUERTA")
        self.assertEqual(command.preposition, "EN")

    def test_verbo_desconocido(self) -> None:
        command = parse_command("bailar")
        self.assertTrue(command.is_error)
        self.assertEqual(command.error_message, "No entiendo ese verbo.")

    def test_salida_de_sesion_especial(self) -> None:
        command = parse_command("salir juego")
        self.assertEqual(command.action, "FIN")


if __name__ == "__main__":
    unittest.main()
