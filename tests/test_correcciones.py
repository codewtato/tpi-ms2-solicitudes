"""Defectos visibles de la versión inicial (ver docs/evidencias/defectos_inicial.txt)."""

from datetime import timedelta

import pytest
from conftest import BEDEL, HOY, nueva

from gestion_solicitudes.consola import ejecutar
from gestion_solicitudes.modelos import ErrorSolicitud, Estado, Solicitud
from gestion_solicitudes.repositorio import RepositorioJson


@pytest.mark.parametrize("entradas", [["2", "abc", "0"], ["3", "abc", "0"], ["3", "1", "abc", "0"]])
def test_def1_un_numero_invalido_no_cierra_el_programa(monkeypatch, capsys, servicio, entradas):
    servicio.registrar(nueva())
    respuestas = iter(entradas)
    monkeypatch.setattr("builtins.input", lambda _="": next(respuestas))
    ejecutar(servicio)
    salida = capsys.readouterr().out
    assert "Error: debe ingresar un numero" in salida and "Hasta luego" in salida


@pytest.mark.parametrize("contenido", ['{"solicitudes": [{"id": 1', "[]", '{"solicitudes": [{"id": 1}], "estudiantes": [], "responsables": []}'])
def test_def2_un_archivo_danado_se_informa_y_no_se_toca(tmp_path, contenido):
    ruta = tmp_path / "datos.json"
    ruta.write_text(contenido, encoding="utf-8")
    with pytest.raises(ErrorSolicitud, match="no se puede interpretar"):
        RepositorioJson(ruta)
    assert ruta.read_text(encoding="utf-8") == contenido


def test_def3_asignar_no_reabre_una_solicitud_cerrada():
    solicitud = Solicitud.crear(1, nueva(), HOY)
    solicitud.asignar(BEDEL)
    solicitud.cambiar_estado(Estado.RESUELTA)
    with pytest.raises(ErrorSolicitud, match="ya esta cerrada"):
        solicitud.asignar(BEDEL)
    assert solicitud.estado is Estado.RESUELTA


def test_def4_lo_que_vence_hoy_todavia_no_esta_vencido():
    solicitud = Solicitud.crear(1, nueva(), HOY)
    assert not solicitud.esta_vencida(solicitud.vence)
    assert solicitud.esta_vencida(solicitud.vence + timedelta(days=1))
