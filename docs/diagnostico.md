# Diagnóstico de la versión inicial

Las ubicaciones se refieren a `main.py` en el tag `estado-inicial`. Evidencias: [`metricas_inicial.txt`](evidencias/metricas_inicial.txt) y [`defectos_inicial.txt`](evidencias/defectos_inicial.txt).

## Calidad externa y calidad interna

| Mirada | Lo que funciona | Lo que falla |
|---|---|---|
| **Externa (usuario)** | Registrar, cambiar estado, asignar responsable, buscar y ver el reporte. Rechaza legajos, tipos y transiciones inválidos. Los datos sobreviven al reinicio. | DEF-1: una letra en un campo numérico cierra el programa. DEF-2: un `datos.json` dañado se reemplaza sin aviso. DEF-3: asignar responsable reabre una solicitud resuelta. DEF-4: lo que vence hoy ya figura vencido. |
| **Interna (equipo)** | Un solo archivo, fácil de encontrar y sin dependencias. | Lógica mezclada con `input` y `print`, sin pruebas unitarias posibles. Reglas repetidas: cada cambio obliga a tocar varios lugares. |

Tres de los cuatro defectos visibles nacen de problemas internos: DEF-1 de repetir la lectura de números sin validar, DEF-2 de un `except` que captura todo y DEF-3 de tener la regla de transición escrita en dos lugares. La calidad interna termina afectando al usuario.

## Indicadores iniciales

| Indicador | Valor | Fuente |
|---|---|---|
| Líneas de código (SLOC) | 219 en 1 archivo | `radon raw` |
| Complejidad ciclomática promedio | 7,0 (B) | `radon cc` |
| Complejidad máxima | 15 en `cambiar_estado` | `radon cc` |
| Función más larga | `registrar`, 40 líneas | Análisis del árbol sintáctico |
| Máximo de parámetros | 9 en `crear_solicitud` | `ruff` PLR0913 |
| Hallazgos de análisis estático | 19 | `ruff` |
| Pruebas automatizadas | 0 | Repositorio |

## Problemas detectados

| ID | Problema | Ubicación | Evidencia | Impacto | Riesgo de mantenimiento | Prioridad |
|---|---|---|---|---|---|---|
| CS-01 | **Módulo Dios / baja cohesión** | `main.py` completo | Interfaz, reglas, reporte y persistencia en 250 líneas | Cualquier cambio obliga a leer y tocar el mismo archivo | Alto: cambios no relacionados se pisan | Alta |
| CS-02 | **Long Method** | `registrar` 45-84, `cambiar_estado` 87-118, `asignar` 121-153 | 40 líneas y CC 14; 32 líneas y CC 15; 33 líneas y CC 10 | Difíciles de entender y probar por partes | Alto: cada regla nueva agranda la función | Alta |
| CS-03 | **Código duplicado** | Búsqueda por id 91-93, 125-127, 135-137. Fila de listado 167, 173, 177 | Mismos bloques copiados hasta 3 veces | Un cambio de formato requiere editar 3 líneas iguales | Alto: una copia queda desactualizada | Alta |
| CS-04 | **Regla de negocio dispersa e inconsistente** | `cambiar_estado` 102-113 y `asignar` 151 | `asignar` fija `en_proceso` sin validar la transición (DEF-3) | Una solicitud resuelta se reabre | Alto: ya produjo un defecto | Alta |
| CS-05 | **Manejo de errores que oculta fallas** | `cargar` 21 | `except:` sin tipo, `ruff` E722 (DEF-2) | Pérdida silenciosa de datos | Alto: el daño no se detecta | Alta |
| CS-06 | **Entrada sin validar** | 89, 123, 133 | `int(input(...))` sin control (DEF-1) | El programa termina con traceback | Medio: se repite en cada campo numérico | Alta |
| CS-07 | **Dependencias rígidas (viola DIP)** | `open` 15 y 35, `datetime.now` 68 y 192, `main()` 250 | La lógica llama directo a archivo, reloj y consola; importar el módulo ya ejecuta el programa | No se puede probar una regla de forma aislada | Alto: frena cualquier otra mejora | Alta |
| CS-08 | **Estado global mutable** | Variables 6-8, `global` 13 | Todas las funciones leen y modifican las mismas listas | Efectos laterales difíciles de seguir | Medio: complica las pruebas | Media |
| CS-09 | **Primitive Obsession y valores mágicos** | `"pendiente"` 80, 102, 194, 202; tipos 56, 69-74, 142; `10` en 64 | Estados y tipos como strings; entidades como dict | Un error de tipeo no se detecta | Medio: los errores aparecen en ejecución | Media |
| CS-10 | **Condicionales que violan OCP** | Plazo 69-74, área 142-145, conteos 194-201 | Agregar un tipo requiere editar varias funciones | Cada tipo nuevo abre varios puntos de cambio | Medio: es fácil olvidar uno | Media |
| CS-11 | **Lista de parámetros larga** | `crear_solicitud` 40 | 9 parámetros posicionales, `ruff` PLR0913 | Es fácil invertir dos valores sin notarlo | Medio | Media |
| CS-12 | **Nombres poco expresivos** | `a, b, c, d, v` 187-191; `t, p, s, x, o` | Hay que leer el código para saber qué es cada variable | Lectura lenta y errores por confusión | Medio | Media |
| CS-13 | **Recursos sin `with` ni encoding** | 15-17 y 35-37 | Un error entre `open` y `close` deja el archivo abierto o incompleto | Posible archivo a medio escribir | Bajo a medio | Baja |
| CS-14 | **Código muerto** | `calcular_total_viejo` 214-218 | Sin llamadas; comentario "lo dejo por las dudas" | Ruido al leer | Bajo | Baja |

## Orden de corrección

1. **Red de seguridad primero.** Sin pruebas no hay forma de saber si un refactoring rompe algo. Como CS-07 impide probar funciones aisladas, se usa una prueba por consola.
2. **Lo que frena a lo demás.** Extraer funciones (CS-02, CS-03), tipar el modelo (CS-09, CS-11) y mover reglas (CS-04, CS-10).
3. **Separación de componentes.** Persistencia, casos de uso y consola (CS-01, CS-07, CS-08, CS-13).
4. **Defectos visibles al final y aparte.** Corregirlos altera el comportamiento, así que no deben mezclarse con el refactoring (CS-05, CS-06, DEF-1 a DEF-4).
