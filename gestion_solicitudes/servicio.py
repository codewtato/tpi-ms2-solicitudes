"""Casos de uso, independientes de la consola y del archivo."""

from datetime import date

from gestion_solicitudes.modelos import ErrorSolicitud, Estado, Solicitud


class ServicioSolicitudes:
    def __init__(self, repositorio, hoy=date.today):
        self._repositorio = repositorio
        self._hoy = hoy

    def registrar(self, nueva):
        self.obtener_estudiante(nueva.legajo)
        solicitudes = self._repositorio.solicitudes
        numero = max((s.id for s in solicitudes), default=0) + 1
        solicitud = Solicitud.crear(numero, nueva, self._hoy())
        solicitudes.append(solicitud)
        self._repositorio.guardar()
        return solicitud

    def cambiar_estado(self, numero, nuevo):
        self.obtener_solicitud(numero).cambiar_estado(nuevo)
        self._repositorio.guardar()

    def asignar(self, numero, numero_responsable):
        solicitud = self.obtener_solicitud(numero)
        responsable = _buscar(
            self._repositorio.responsables, "id", numero_responsable, "no existe el responsable"
        )
        solicitud.asignar(responsable)
        self._repositorio.guardar()
        return responsable

    def obtener_estudiante(self, legajo):
        return _buscar(self._repositorio.estudiantes, "legajo", legajo, "no existe el estudiante")

    def obtener_solicitud(self, numero):
        return _buscar(self._repositorio.solicitudes, "id", numero, "no existe la solicitud")

    def responsables(self):
        return self._repositorio.responsables

    def buscar(self, estado=None, legajo=None):
        return [
            s
            for s in self._repositorio.solicitudes
            if estado in (None, s.estado.value) and legajo in (None, s.legajo)
        ]

    def reporte_general(self):
        return resumir(self._repositorio.solicitudes, self._hoy())


def resumir(solicitudes, hoy):
    """Recibe solo la lista que necesita, así se puede probar sin repositorio."""
    conteo = {estado: sum(s.estado is estado for s in solicitudes) for estado in Estado}
    return [
        f"Total: {len(solicitudes)}",
        f"Pendientes: {conteo[Estado.PENDIENTE]}",
        f"En proceso: {conteo[Estado.EN_PROCESO]}",
        f"Resueltas: {conteo[Estado.RESUELTA]}",
        f"Rechazadas: {conteo[Estado.RECHAZADA]}",
        f"Vencidas: {sum(s.esta_vencida(hoy) for s in solicitudes)}",
    ]


def _buscar(elementos, atributo, valor, error):
    for elemento in elementos:
        if getattr(elemento, atributo) == valor:
            return elemento
    raise ErrorSolicitud(error)
