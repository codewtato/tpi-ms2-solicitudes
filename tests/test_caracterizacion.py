"""Red de seguridad: la consola y el JSON deben seguir igual que en la versión inicial.

Los archivos de tests/dorados se generaron una sola vez sobre el tag estado-inicial,
ejecutando este archivo con `python tests/test_caracterizacion.py`. No hay que
regenerarlos después de refactorizar: compararían el código consigo mismo.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ESCENARIO = RAIZ / "tests" / "escenarios" / "principal.txt"
DORADO_CONSOLA = RAIZ / "tests" / "dorados" / "principal_consola.txt"
DORADO_DATOS = RAIZ / "tests" / "dorados" / "principal_datos.json"


def normalizar(texto):
    """Reemplaza las fechas, que dependen del día en que se corre la prueba."""
    return re.sub(r"\d{4}-\d{2}-\d{2}", "<FECHA>", texto)


def ejecutar(carpeta):
    """Corre el programa como lo usa una persona y devuelve la consola y el JSON."""
    resultado = subprocess.run(
        [sys.executable, str(RAIZ / "main.py")],
        input=ESCENARIO.read_text(encoding="utf-8"),
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=carpeta,
        timeout=30,
        check=True,
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    datos = json.loads((Path(carpeta) / "datos.json").read_text(encoding="utf-8"))
    return normalizar(resultado.stdout), normalizar(json.dumps(datos, indent=2, sort_keys=True)) + "\n"


def test_el_comportamiento_externo_no_cambia(tmp_path):
    consola, datos = ejecutar(tmp_path)
    assert consola == DORADO_CONSOLA.read_text(encoding="utf-8")
    assert datos == DORADO_DATOS.read_text(encoding="utf-8")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as temporal:
        consola, datos = ejecutar(temporal)
    DORADO_CONSOLA.write_text(consola, encoding="utf-8")
    DORADO_DATOS.write_text(datos, encoding="utf-8")
