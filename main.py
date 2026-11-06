"""Punto de entrada: conecta las piezas del sistema y lo ejecuta."""

import sys

from gestion_solicitudes.consola import ejecutar
from gestion_solicitudes.modelos import ErrorSolicitud
from gestion_solicitudes.repositorio import RepositorioJson
from gestion_solicitudes.servicio import ServicioSolicitudes

ARCHIVO_DATOS = "datos.json"


def main():
    try:
        ejecutar(ServicioSolicitudes(RepositorioJson(ARCHIVO_DATOS)))
    except ErrorSolicitud as error:
        print(f"Error: {error}")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nHasta luego")
    return 0


if __name__ == "__main__":
    sys.exit(main())
