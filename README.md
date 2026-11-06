# Gestión de Solicitudes Académicas

Sistema por consola para registrar y seguir solicitudes de estudiantes. Es el caso de estudio del Trabajo Práctico Integrador de Metodología de Sistemas II (Comisión 13): parte de un prototipo que funciona pero está mal estructurado, y lo mejora mediante refactoring seguro sin alterar su comportamiento externo.

**Integrantes:** Matías D'Agostino y Facundo Cufré.

## Funcionalidades

- Registrar solicitudes con tipo, prioridad y descripción. El plazo se calcula según el tipo.
- Cambiar el estado, respetando las transiciones permitidas.
- Asignar un responsable del área que corresponde a cada tipo.
- Buscar por estado o legajo.
- Ver un reporte general.
- Guardar los datos en un archivo JSON.

## Tecnologías

Python 3.10 o superior, solo con la biblioteca estándar. Se probó con Python 3.14 en Linux. Las pruebas usan `pytest`.

## Instalación y uso

```bash
git clone <URL-DEL-REPOSITORIO>
cd gestion-solicitudes
python main.py
```

Hay que ejecutar `main.py`: los archivos de `gestion_solicitudes/` no se abren por separado.

Los datos se guardan en `datos.json` en la carpeta desde donde se ejecuta. La primera vez arranca con datos de ejemplo, todos sintéticos. Para registrar una solicitud se pueden usar los legajos `1001` o `1002`.

## Pruebas

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

## Estructura

```text
main.py                  punto de entrada
gestion_solicitudes/
  consola.py             interacción con el usuario
  servicio.py            casos de uso y reporte
  modelos.py             entidades y reglas de negocio
  repositorio.py         persistencia
tests/                   pruebas, escenarios y archivos dorados
docs/                    diagnóstico, decisiones, pruebas, code review y evidencias
```

## Documentación

- [Diagnóstico de calidad y code smells](docs/diagnostico.md)
- [Decisiones técnicas, refactorings y SOLID](docs/decisiones.md)
- [Pruebas y verificación](docs/pruebas.md)
- [Checklist y resultados del code review](docs/code_review.md)
- [Evidencias](docs/evidencias/)

## Versiones

| Tag | Hito |
|---|---|
| `estado-inicial` | Sistema base, con los problemas originales |
| `etapa-diagnostico` | Diagnóstico de calidad y code smells |
| `etapa-refactoring` | Refactorings terminados, con la misma salida que la versión inicial |
| `etapa-pruebas` | Pruebas unitarias, correcciones y verificación |
| `etapa-docs` | Documentación del trabajo |
| `estadorefactorizado` | Estado final del código (también `estado-refactorizado`) |

Para ver la versión inicial: `git switch --detach estado-inicial`. Para volver: `git switch main`.
