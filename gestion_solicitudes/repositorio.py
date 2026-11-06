"""Persistencia en un archivo JSON. El resto del sistema no conoce el archivo."""

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from gestion_solicitudes.modelos import (
    ErrorSolicitud,
    Estado,
    Estudiante,
    Prioridad,
    Responsable,
    Solicitud,
    Tipo,
)


class RepositorioJson:
    def __init__(self, ruta):
        self._ruta = Path(ruta)
        self.solicitudes, self.estudiantes, self.responsables = self._leer()

    def guardar(self):
        datos = {
            "solicitudes": [_solicitud_a_dict(s) for s in self.solicitudes],
            "estudiantes": [asdict(e) for e in self.estudiantes],
            "responsables": [asdict(r) for r in self.responsables],
        }
        # Se escribe aparte y se reemplaza al final: un corte no deja el archivo a medias.
        temporal = self._ruta.with_name(self._ruta.name + ".tmp")
        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2)
        temporal.replace(self._ruta)

    def _leer(self):
        try:
            with self._ruta.open(encoding="utf-8") as archivo:
                datos = json.load(archivo)
            return (
                [_solicitud_desde_dict(s) for s in datos["solicitudes"]],
                [Estudiante(**e) for e in datos["estudiantes"]],
                [Responsable(**r) for r in datos["responsables"]],
            )
        except FileNotFoundError:
            return [], _estudiantes_de_ejemplo(), _responsables_de_ejemplo()
        except (ValueError, KeyError, TypeError) as error:
            raise ErrorSolicitud(
                f"no se puede interpretar {self._ruta}: revise o restaure el archivo"
            ) from error


def _estudiantes_de_ejemplo():
    return [Estudiante("1001", "Ana Prueba"), Estudiante("1002", "Bruno Ejemplo")]


def _responsables_de_ejemplo():
    return [
        Responsable(1, "Diego Bedel", "Bedelia"),
        Responsable(2, "Elena Secretaria", "Secretaria"),
    ]


def _solicitud_desde_dict(datos):
    return Solicitud(
        datos["id"],
        datos["legajo"],
        Tipo(datos["tipo"]),
        Prioridad(datos["prioridad"]),
        datos["descripcion"],
        date.fromisoformat(datos["fecha"]),
        date.fromisoformat(datos["vence"]),
        Estado(datos["estado"]),
        datos["responsable"],
    )


def _solicitud_a_dict(solicitud):
    return {
        **asdict(solicitud),
        "tipo": solicitud.tipo.value,
        "prioridad": solicitud.prioridad.value,
        "fecha": solicitud.fecha.isoformat(),
        "vence": solicitud.vence.isoformat(),
        "estado": solicitud.estado.value,
    }
