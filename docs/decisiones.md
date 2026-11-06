# Decisiones técnicas

## Diseño resultante

```text
main.py                   conecta las piezas
  └─ consola.py           interacción con el usuario
       └─ servicio.py     casos de uso y reporte
            ├─ modelos.py      entidades y reglas de negocio
            └─ repositorio.py  persistencia en JSON
```

`modelos.py` no conoce la consola ni el archivo, y `servicio.py` recibe el repositorio por constructor.

## Refactorings

Cada uno está en su propio commit, con la prueba de caracterización en verde.

| # | Técnica | Commit | Antes | Después | Corrige |
|---|---|---|---|---|---|
| R1 | **Extract Method** | `a490438` | `registrar` de 40 líneas; fila copiada 3 veces | Funciones cortas como `imprimir_filas` y `calcular_plazo` | CS-02, CS-03, CS-12, CS-14 |
| R2 | **Replace Type Code con Enum** y dict por dataclass | `1266140` | `"pendiente"` y `s["estado"]` | `Estado.PENDIENTE` y `solicitud.estado` | CS-09 |
| R3 | **Introduce Parameter Object** | `acc0b11` | `crear_solicitud` con 9 parámetros | `NuevaSolicitud` | CS-11 |
| R4 | **Move Method** | `e2e0371` | Reglas en funciones de consola y `if/elif` por tipo | `Solicitud.cambiar_estado`, `esta_vencida` y `REGLAS` | CS-04, CS-10 |
| R5 | **Extract Class** para persistencia | `c0150ea` | Listas globales y `open` directo | `RepositorioJson` | CS-08, CS-13 |
| R6 | **Extract Class** para casos de uso y consola | `d84a528` | `main.py` de 250 líneas | `main.py` de 11 líneas, `ServicioSolicitudes` y `consola.py` | CS-01, CS-07 |

CS-05 y CS-06 no se pueden resolver sin cambiar el comportamiento, así que se corrigieron aparte como DEF-2 y DEF-1. CS-04 se completó con DEF-3: R4 reunió la regla en un solo lugar y la corrección agregó la validación que faltaba.

## Principios SOLID

| Principio | Aplicación | Cómo se verifica |
|---|---|---|
| **SRP** | Un motivo de cambio por módulo: interacción, casos de uso, reglas y persistencia | `input` solo aparece en `consola.py` |
| **OCP** | Un tipo nuevo es un valor del Enum y una entrada en `REGLAS` | `test_cr07_todo_tipo_tiene_su_regla` controla la tabla |
| **LSP** | `RepositorioJson` y el repositorio en memoria de las pruebas son intercambiables | `test_cualquier_repositorio_sirve_al_servicio` corre sobre ambos |
| **ISP** | `resumir` recibe solo la lista que necesita, no todo el repositorio | `test_el_reporte_cuenta_estados_y_solo_vencen_las_abiertas` |
| **DIP** | El servicio recibe el repositorio y el reloj; `main.py` elige la implementación | `test_sistema.py` funciona sin archivos y con fecha fija |

## Clean Code

| Aspecto | Antes | Después |
|---|---|---|
| Nombres | `a, b, c, d, v`; `t, p, s, x, o` | `solicitudes`, `prioridad`, `numero_responsable` |
| Funciones | Hasta 40 líneas | Hasta 25 líneas |
| Errores | `except:` y `print` con `return` | `ErrorSolicitud`, capturado en un solo lugar |
| Valores mágicos | `10`, `5`, `30`, `"Bedelia"` dentro de la lógica | `LARGO_MINIMO_DESCRIPCION`, `REGLAS` |
| Comentarios | "ya no se usa, lo dejo por las dudas" | Código eliminado |
| Recursos | `open` y `close` manuales | `with`, encoding explícito y escritura atómica |

## Decisiones y alternativas

| Decisión | Alternativa descartada | Motivo |
|---|---|---|
| Sin `Protocol` ni clases abstractas | Interfaces explícitas | Python permite sustituir el repositorio sin declararlas; agregarían código sin beneficio en un sistema tan chico |
| Una sola excepción, `ErrorSolicitud` | Una jerarquía de errores | La consola trata a todos igual: muestra el mensaje |
| Reporte como función | Una clase por reporte | Hay un solo reporte; una jerarquía sería diseño para un futuro hipotético |
| Conservar el formato del JSON | Normalizar los datos | Los datos existentes siguen sirviendo y la comparación es directa |
| Mantener mensajes sin tildes | Corregirlos durante el refactoring | Cambiarían la salida |
| Sin base de datos ni web | SQLite o Flask | No aportan a mejorar el diseño de un módulo acotado |

## Métricas antes y después

| Indicador | `estado-inicial` | Final |
|---|---|---|
| Complejidad ciclomática promedio | 7,0 | 2,2 |
| Complejidad máxima por función | 15 | 6 |
| Función más larga | 40 líneas | 25 líneas |
| Máximo de parámetros | 9 | 4 |
| Hallazgos de `ruff` con las mismas reglas | 19 | 1 (justificado en CR-08) |
| Pruebas automatizadas | 0 | 35 |
| Cobertura de línea | Sin medir, no había pruebas | 83 % |
| Líneas de código (SLOC) | 219 | 324 |

El código creció: separar responsabilidades agrega clases y firmas. El beneficio no está en escribir menos, sino en poder entender, probar y cambiar cada parte por separado.

La cobertura mide solo pruebas en el mismo proceso. El 53 % de `consola.py` subestima el valor real, porque la prueba de caracterización la ejercita como proceso aparte y esa ejecución no se contabiliza. Evidencia: [`metricas_inicial.txt`](evidencias/metricas_inicial.txt), [`metricas_final.txt`](evidencias/metricas_final.txt) y [`cobertura.txt`](evidencias/cobertura.txt).
