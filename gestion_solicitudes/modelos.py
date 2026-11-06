"""Entidades del dominio."""

from dataclasses import dataclass
from datetime import date
from enum import Enum


class Estado(Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    RESUELTA = "resuelta"
    RECHAZADA = "rechazada"


class Prioridad(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


class Tipo(Enum):
    CERTIFICADO = "certificado"
    EQUIVALENCIA = "equivalencia"
    RECLAMO = "reclamo"


@dataclass(frozen=True)
class Estudiante:
    legajo: str
    nombre: str


@dataclass(frozen=True)
class Responsable:
    id: int
    nombre: str
    area: str


@dataclass(frozen=True)
class NuevaSolicitud:
    """Lo que aporta quien registra una solicitud; el resto lo calcula el sistema."""

    legajo: str
    tipo: Tipo
    prioridad: Prioridad
    descripcion: str


@dataclass
class Solicitud:
    id: int
    legajo: str
    tipo: Tipo
    prioridad: Prioridad
    descripcion: str
    fecha: date
    vence: date
    estado: Estado = Estado.PENDIENTE
    responsable: int | None = None
