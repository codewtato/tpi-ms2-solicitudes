"""Punto de entrada: conecta las piezas del sistema y lo ejecuta."""

from gestion_solicitudes.consola import ejecutar
from gestion_solicitudes.repositorio import RepositorioJson
from gestion_solicitudes.servicio import ServicioSolicitudes

ARCHIVO_DATOS = "datos.json"


if __name__ == "__main__":
    ejecutar(ServicioSolicitudes(RepositorioJson(ARCHIVO_DATOS)))
