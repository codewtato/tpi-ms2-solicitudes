"""Reglas, casos de uso y persistencia, sin consola y con fecha fija."""

from datetime import timedelta

import pytest
from conftest import BEDEL, HOY, SECRETARIA, RepositorioEnMemoria, nueva

from gestion_solicitudes.consola import ejecutar
from gestion_solicitudes.modelos import ErrorSolicitud, Estado, NuevaSolicitud, Prioridad, Solicitud, Tipo
from gestion_solicitudes.repositorio import RepositorioJson
from gestion_solicitudes.servicio import ServicioSolicitudes, resumir


def solicitud(estado=Estado.PENDIENTE, tipo=Tipo.CERTIFICADO, prioridad=Prioridad.MEDIA):
    creada = Solicitud.crear(1, nueva(tipo, prioridad), HOY)
    creada.estado = estado
    return creada


@pytest.mark.parametrize(("tipo", "dias"), [(Tipo.CERTIFICADO, 5), (Tipo.EQUIVALENCIA, 30), (Tipo.RECLAMO, 7)])
def test_el_vencimiento_depende_del_tipo(tipo, dias):
    assert solicitud(tipo=tipo).vence == HOY + timedelta(days=dias)


def test_el_reclamo_siempre_es_prioridad_alta():
    assert solicitud(tipo=Tipo.RECLAMO, prioridad=Prioridad.BAJA).prioridad is Prioridad.ALTA


def test_la_descripcion_corta_se_rechaza():
    with pytest.raises(ErrorSolicitud, match="al menos 10"):
        NuevaSolicitud("1001", Tipo.CERTIFICADO, Prioridad.MEDIA, "corta")


@pytest.mark.parametrize(
    ("origen", "destino"),
    [(Estado.PENDIENTE, Estado.EN_PROCESO), (Estado.PENDIENTE, Estado.RECHAZADA), (Estado.EN_PROCESO, Estado.RECHAZADA)],
)
def test_transiciones_permitidas(origen, destino):
    actual = solicitud(origen)
    actual.cambiar_estado(destino)
    assert actual.estado is destino


@pytest.mark.parametrize(
    ("origen", "destino", "mensaje"),
    [
        (Estado.PENDIENTE, Estado.RESUELTA, "no se puede pasar"),
        (Estado.EN_PROCESO, Estado.RESUELTA, "sin responsable"),
        (Estado.RESUELTA, Estado.RECHAZADA, "ya esta cerrada"),
        (Estado.RECHAZADA, Estado.EN_PROCESO, "ya esta cerrada"),
    ],
)
def test_transiciones_prohibidas(origen, destino, mensaje):
    actual = solicitud(origen)
    with pytest.raises(ErrorSolicitud, match=mensaje):
        actual.cambiar_estado(destino)
    assert actual.estado is origen


def test_asignar_exige_el_area_correcta():
    actual = solicitud()
    with pytest.raises(ErrorSolicitud, match="lo atiende Bedelia"):
        actual.asignar(SECRETARIA)
    actual.asignar(BEDEL)
    assert (actual.responsable, actual.estado) == (BEDEL.id, Estado.EN_PROCESO)


def test_el_servicio_usa_la_fecha_inyectada_y_numera_en_orden(servicio):
    assert [servicio.registrar(nueva()).id, servicio.registrar(nueva()).id] == [1, 2]
    assert servicio.obtener_solicitud(1).fecha == HOY


def test_el_servicio_informa_lo_inexistente(servicio):
    with pytest.raises(ErrorSolicitud, match="no existe el estudiante"):
        servicio.registrar(nueva(legajo="9999"))
    with pytest.raises(ErrorSolicitud, match="no existe la solicitud"):
        servicio.cambiar_estado(99, Estado.RECHAZADA)


def test_el_reporte_cuenta_estados_y_solo_vencen_las_abiertas():
    solicitudes = [solicitud(), solicitud(Estado.EN_PROCESO), solicitud(Estado.RESUELTA), solicitud(Estado.RECHAZADA)]
    assert resumir(solicitudes, HOY + timedelta(days=6)) == [
        "Total: 4", "Pendientes: 1", "En proceso: 1", "Resueltas: 1", "Rechazadas: 1", "Vencidas: 2",
    ]


@pytest.fixture(params=["memoria", "json"])
def repositorio(request, tmp_path):
    return RepositorioEnMemoria() if request.param == "memoria" else RepositorioJson(tmp_path / "datos.json")


def test_cualquier_repositorio_sirve_al_servicio(repositorio):
    servicio = ServicioSolicitudes(repositorio, hoy=lambda: HOY)
    creada = servicio.registrar(nueva())
    servicio.asignar(creada.id, BEDEL.id)
    servicio.cambiar_estado(creada.id, Estado.RESUELTA)
    assert servicio.obtener_solicitud(creada.id).estado is Estado.RESUELTA


def test_los_datos_sobreviven_a_un_reinicio(tmp_path):
    ruta = tmp_path / "datos.json"
    ServicioSolicitudes(RepositorioJson(ruta), hoy=lambda: HOY).registrar(nueva())
    assert RepositorioJson(ruta).solicitudes == [Solicitud.crear(1, nueva(), HOY)]


def test_la_consola_informa_el_error_y_el_menu_sigue(monkeypatch, capsys, servicio):
    respuestas = iter(["1", "9999", "0"])
    monkeypatch.setattr("builtins.input", lambda _="": next(respuestas))
    ejecutar(servicio)
    salida = capsys.readouterr().out
    assert "Error: no existe el estudiante" in salida and "Hasta luego" in salida
