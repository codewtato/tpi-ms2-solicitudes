# Pruebas y verificación

## Estrategia

La versión inicial no admitía pruebas unitarias porque importar `main.py` ejecutaba el programa. La verificación siguió este orden:

1. **Caracterización antes de tocar nada.** Se ejecutaron escenarios por consola sobre `estado-inicial` y se guardaron la salida y el JSON como archivos dorados. Las pruebas comparan el texto completo y solo normalizan las fechas.
2. **Refactoring con la red activa.** La prueba de caracterización pasa en cada commit del refactoring.
3. **Pruebas unitarias después.** El nuevo diseño permite probar reglas con repositorio en memoria y fecha fija.
4. **Defectos con prueba previa.** Primero una prueba que falla; después, la corrección.

## Archivos de prueba

| Archivo | Qué verifica | Tipo |
|---|---|---|
| `tests/test_caracterizacion.py` | Consola y JSON contra la versión inicial, en 3 escenarios | Caracterización |
| `tests/test_sistema.py` | Plazos, prioridades, transiciones, áreas, reporte, persistencia y consola | Unitaria e integración |
| `tests/test_correcciones.py` | Defectos corregidos | Regresión |

## Casos funcionales principales

| Caso | Entrada | Resultado esperado |
|---|---|---|
| Registrar válida | Legajo 1001, certificado, media | Número 1, pendiente, vence en 5 días |
| Legajo inexistente | 9999 | Error y no se guarda |
| Descripción corta | "corta" | Error de largo mínimo |
| Reclamo con prioridad baja | reclamo, baja | Se guarda con prioridad alta |
| Transición prohibida | Pendiente a resuelta | Error y el estado no cambia |
| Resolver sin responsable | En proceso sin responsable | Error |
| Responsable de otra área | Equivalencia con Bedelía | Error que indica el área correcta |
| Reinicio del programa | Datos guardados | Los datos siguen disponibles |
| Reporte de vencidas | Abiertas y cerradas con fechas pasadas | Cuenta solo las abiertas |

## Evidencias

| Evidencia | Archivo |
|---|---|
| Suite completa (35 pruebas) | [`pruebas_resultado.txt`](evidencias/pruebas_resultado.txt) |
| Caracterización en cada commit | [`verificacion_por_commit.txt`](evidencias/verificacion_por_commit.txt) |
| Defectos antes y después de corregir (8 fallan, 8 pasan) | [`correcciones_antes.txt`](evidencias/correcciones_antes.txt), [`correcciones_despues.txt`](evidencias/correcciones_despues.txt) |
| Sesiones de consola de ambas versiones (idénticas) | [`demo_consola_inicial.txt`](evidencias/demo_consola_inicial.txt), [`demo_consola_final.txt`](evidencias/demo_consola_final.txt) |

Para repetir la verificación en cualquier punto del historial:

```bash
python -m pytest
git switch --detach etapa-refactoring
python -m pytest
git switch main
```

## Cambios de comportamiento deliberados

Hasta `etapa-refactoring` la salida no cambia. Los únicos cambios visibles están después, en commits `fix`:

| Situación | Antes | Después |
|---|---|---|
| DEF-1: letra en un campo numérico | El programa termina con traceback | Mensaje de error y el menú sigue |
| DEF-2: `datos.json` dañado | Se reemplaza sin aviso | Mensaje de error, código de salida 1 y archivo intacto |
| DEF-3: asignar responsable a una cerrada | Se reabre | Se rechaza |
| DEF-4: solicitud que vence hoy | Figura vencida | Figura vencida recién desde mañana |

## Límites

- Se ejecutó solo en Linux con Python 3.14.
- Los archivos dorados cubren los escenarios escritos, no todas las combinaciones posibles.
