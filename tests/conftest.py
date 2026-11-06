"""Datos comunes y un repositorio en memoria que reemplaza al de archivo."""

from datetime import date

import pytest

from gestion_solicitudes.modelos import Estudiante, NuevaSolicitud, Prioridad, Responsable, Tipo
from gestion_solicitudes.servicio import ServicioSolicitudes

HOY = date(2026, 3, 10)
BEDEL = Responsable(1, "Diego Bedel", "Bedelia")
SECRETARIA = Responsable(2, "Elena Secretaria", "Secretaria")


def nueva(tipo=Tipo.CERTIFICADO, prioridad=Prioridad.MEDIA, legajo="1001"):
    return NuevaSolicitud(legajo, tipo, prioridad, "Descripcion de prueba")


class RepositorioEnMemoria:
    def __init__(self):
        self.solicitudes = []
        self.estudiantes = [Estudiante("1001", "Ana Prueba")]
        self.responsables = [BEDEL, SECRETARIA]

    def guardar(self):
        pass


@pytest.fixture
def servicio():
    return ServicioSolicitudes(RepositorioEnMemoria(), hoy=lambda: HOY)
