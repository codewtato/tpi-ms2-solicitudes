"""Red de seguridad: la consola y el JSON deben seguir igual que en la versión inicial.

Los archivos de tests/dorados se generaron una sola vez sobre el tag estado-inicial,
ejecutando este archivo con `python tests/test_caracterizacion.py`. No hay que
regenerarlos después de refactorizar: compararían el código consigo mismo.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ESCENARIOS = RAIZ / "tests" / "escenarios"
DORADOS = RAIZ / "tests" / "dorados"


def normalizar(texto):
    return re.sub(r"\d{4}-\d{2}-\d{2}", "<FECHA>", texto)


def ejecutar(nombre, carpeta):
    """Corre el programa como lo usa una persona y devuelve la consola y el JSON."""
    resultado = subprocess.run(
        [sys.executable, str(RAIZ / "main.py")],
        input=(ESCENARIOS / f"{nombre}.txt").read_text(encoding="utf-8"),
        capture_output=True, text=True, encoding="utf-8", cwd=carpeta, timeout=30, check=True,
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    datos = json.loads((Path(carpeta) / "datos.json").read_text(encoding="utf-8"))
    return normalizar(resultado.stdout), normalizar(json.dumps(datos, indent=2, sort_keys=True)) + "\n"


def correr_todo(carpeta_base):
    """Principal y reinicio comparten carpeta: el segundo comprueba que los datos persisten."""
    resultados = {}
    compartida = Path(carpeta_base) / "compartida"
    compartida.mkdir()
    for nombre in ("principal", "reinicio"):
        resultados[nombre] = ejecutar(nombre, compartida)
    vencidas = Path(carpeta_base) / "vencidas"
    vencidas.mkdir()
    shutil.copy(ESCENARIOS / "vencidas_datos.json", vencidas / "datos.json")
    resultados["vencidas"] = ejecutar("vencidas", vencidas)
    return resultados


def test_el_comportamiento_externo_no_cambia(tmp_path):
    for nombre, (consola, datos) in correr_todo(tmp_path).items():
        assert consola == (DORADOS / f"{nombre}_consola.txt").read_text(encoding="utf-8")
        assert datos == (DORADOS / f"{nombre}_datos.json").read_text(encoding="utf-8")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as temporal:
        for nombre, (consola, datos) in correr_todo(temporal).items():
            (DORADOS / f"{nombre}_consola.txt").write_text(consola, encoding="utf-8")
            (DORADOS / f"{nombre}_datos.json").write_text(datos, encoding="utf-8")
