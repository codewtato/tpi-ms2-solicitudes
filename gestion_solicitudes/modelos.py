"""Entidades del dominio y reglas de negocio que les pertenecen."""

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum

LARGO_MINIMO_DESCRIPCION = 10


class ErrorSolicitud(Exception):
    """Error de negocio; su mensaje se muestra al usuario."""


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
class Regla:
    plazo_dias: int
    area: str
    prioridad_fija: Prioridad | None = None


# Agregar un tipo de solicitud es sumarlo al Enum y a esta tabla.
REGLAS = {
    Tipo.CERTIFICADO: Regla(5, "Bedelia"),
    Tipo.EQUIVALENCIA: Regla(30, "Secretaria"),
    Tipo.RECLAMO: Regla(7, "Secretaria", prioridad_fija=Prioridad.ALTA),
}

TRANSICIONES = {
    Estado.PENDIENTE: (Estado.EN_PROCESO, Estado.RECHAZADA),
    Estado.EN_PROCESO: (Estado.RESUELTA, Estado.RECHAZADA),
}


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

    def __post_init__(self):
        if len(self.descripcion) < LARGO_MINIMO_DESCRIPCION:
            raise ErrorSolicitud(f"la descripcion debe tener al menos {LARGO_MINIMO_DESCRIPCION} caracteres")


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

    @classmethod
    def crear(cls, numero, nueva, hoy):
        regla = REGLAS[nueva.tipo]
        vence = hoy + timedelta(days=regla.plazo_dias)
        prioridad = regla.prioridad_fija or nueva.prioridad
        return cls(numero, nueva.legajo, nueva.tipo, prioridad, nueva.descripcion, hoy, vence)

    @property
    def esta_abierta(self):
        return self.estado in TRANSICIONES

    def esta_vencida(self, hoy):
        return self.esta_abierta and self.vence < hoy

    def cambiar_estado(self, nuevo):
        if not self.esta_abierta:
            raise ErrorSolicitud("la solicitud ya esta cerrada")
        if nuevo not in TRANSICIONES[self.estado]:
            raise ErrorSolicitud(f"no se puede pasar de {self.estado.value} a {nuevo.value}")
        if nuevo is Estado.RESUELTA and self.responsable is None:
            raise ErrorSolicitud("no se puede resolver sin responsable")
        self.estado = nuevo

    def asignar(self, responsable):
        if not self.esta_abierta:
            raise ErrorSolicitud("la solicitud ya esta cerrada")
        area = REGLAS[self.tipo].area
        if responsable.area != area:
            raise ErrorSolicitud(f"ese tipo lo atiende {area}")
        self.responsable = responsable.id
        self.estado = Estado.EN_PROCESO
