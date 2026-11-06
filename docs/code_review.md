# Code review

Revisión técnica de la versión refactorizada, hecha sobre el commit del tag `etapa-pruebas`. Cada sospecha se reprodujo antes de registrarse como hallazgo.

## Checklist técnico

| # | Criterio | Resultado inicial | Hallazgo o evidencia |
|---|---|---|---|
| 1 | Cada módulo tiene una sola responsabilidad (SRP) | **Observado** | CR-04 |
| 2 | Agregar un tipo no obliga a editar el flujo (OCP) | **Observado** | CR-07 |
| 3 | Las implementaciones son intercambiables (LSP) | Cumple | `test_cualquier_repositorio_sirve_al_servicio` |
| 4 | Cada cliente recibe solo lo que usa (ISP) | Cumple | `resumir` recibe una lista |
| 5 | Lo interno no depende de detalles concretos (DIP) | Cumple | El servicio recibe repositorio y reloj |
| 6 | Nombres expresivos | Cumple | `ruff` N solo observa CR-08 |
| 7 | Funciones cortas, con complejidad de 10 o menos | Cumple | Máximo: CC 9 antes de CR-04 |
| 8 | Sin código muerto | Cumple | Revisión manual y `ruff` F |
| 9 | Los errores se informan sin ocultar fallas | **Observado** | CR-03, CR-06 |
| 10 | Las entradas se validan | **Observado** | CR-02 |
| 11 | Los datos se identifican sin ambigüedad | **Observado** | CR-01 |
| 12 | Hay pruebas para reglas y casos de error | Cumple | Suite en verde |
| 13 | El comportamiento externo se mantuvo | Cumple | `verificacion_por_commit.txt` |
| 14 | Los datos son sintéticos | Cumple | `repositorio.py` |
| 15 | Formato y documentación coherentes | **Observado** | CR-05, CR-11 |
| 16 | Los commits son pequeños y explican el motivo | Cumple | `git log` |

## Hallazgos y feedback

| ID | Severidad | Ubicación | Observación | Por qué importa | Sugerencia | Decisión | Estado |
|---|---|---|---|---|---|---|---|
| CR-01 | Alta | `ServicioSolicitudes.registrar` | Con ids `[1, 3]`, el nuevo id es 3 y quedan dos solicitudes con el mismo número | La segunda no se puede consultar ni modificar | Usar el id máximo más 1 | Aceptada | Corregida |
| CR-02 | Media | `NuevaSolicitud` | Una descripción de 15 espacios cumple el largo mínimo | La regla no logra su objetivo | Medir el texto sin espacios en los extremos | Aceptada | Corregida |
| CR-03 | Media | `main.py` | Ctrl+C o el cierre de la entrada terminan con traceback | Mala experiencia y ruido al diagnosticar | Capturar esos casos en el punto de entrada | Aceptada | Corregida |
| CR-04 | Media | `consola.buscar` | El filtro de búsqueda estaba en la interfaz (CC 9) | Mezcla interfaz y lógica | Mover el filtro al servicio | Aceptada | Corregida |
| CR-05 | Baja | Todo el código | `ruff` marca líneas largas e imports sin ordenar | Lectura despareja | Aplicar un formato único | Aceptada | Corregida |
| CR-06 | Media | `RepositorioJson.guardar` | Sin permisos de escritura termina con `PermissionError`, con el cambio ya aplicado en memoria | Termina con traceback, aunque el fallo es visible | Manejar `OSError` y revertir en memoria | Postergada: requiere definir qué se revierte; es un uso local de un solo usuario | Pendiente |
| CR-07 | Baja | `REGLAS` | Un tipo sin regla fallaría recién en ejecución | Riesgo al agregar un tipo | Agregar una prueba que lo controle | Aceptada | Corregida |
| CR-08 | Baja | `modelos.py` | `ruff` N818 pide que la excepción termine en `Error` | Convención en inglés; el nombre ya es claro | Ninguna | Rechazada con justificación | Sin cambios |
| CR-09 | Baja | `consola.registrar` | Busca el estudiante en la consola y otra vez en el servicio | Consulta repetida | Ninguna: avisa antes de pedir el resto, como la versión inicial | Rechazada con justificación | Sin cambios |
| CR-10 | Baja | `RepositorioJson` | Expone sus listas como atributos públicos | Menos encapsulamiento | Ninguna: solo las usa el servicio, y ocultarlas agrega código sin beneficio en un sistema tan chico | Rechazada con justificación | Sin cambios |
| CR-11 | Baja | `consola.py`, README | El docstring decía que era el único módulo con `print` (`main.py` también lo usa) y el README seguía describiendo la versión inicial | La documentación no coincide con el código | Corregir ambos | Aceptada | Corregida |

Evidencia: [`review_antes.txt`](evidencias/review_antes.txt) y [`review_despues.txt`](evidencias/review_despues.txt).

## Criterios de aceptación técnica

| Criterio | Umbral | Resultado | ¿Cumple? |
|---|---|---|---|
| Pruebas automatizadas | 100 % en verde | 35 de 35 | Sí |
| Comportamiento externo | Caracterización en verde en cada commit | Todos en verde | Sí |
| Complejidad por función | CC de 10 o menos | Máximo 6 | Sí |
| Largo de función | 25 líneas o menos | Máximo 25 | Sí |
| Parámetros por función | 5 o menos | Máximo 4 | Sí |
| Análisis estático | Sin errores, salvo excepciones justificadas | 1 hallazgo, rechazado en CR-08 | Sí |
| Hallazgos de severidad alta | Ninguno abierto | Ninguno | Sí |
| Pendientes | Registrados y justificados | CR-06 | Sí |
