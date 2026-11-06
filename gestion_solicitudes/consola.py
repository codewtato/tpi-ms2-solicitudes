"""Interfaz por consola: toda la interacción con el usuario durante el uso del sistema."""

from gestion_solicitudes.modelos import (
    ErrorSolicitud,
    Estado,
    NuevaSolicitud,
    Prioridad,
    Tipo,
)

ESTADOS_DESTINO = (Estado.EN_PROCESO, Estado.RESUELTA, Estado.RECHAZADA)


def ejecutar(servicio):
    acciones = {
        "1": ("Registrar solicitud", registrar),
        "2": ("Cambiar estado", cambiar_estado),
        "3": ("Asignar responsable", asignar),
        "4": ("Buscar solicitudes", buscar),
        "5": ("Reporte general", reporte),
    }
    while True:
        print("")
        print("=== Solicitudes Academicas ===")
        for clave, (titulo, _) in acciones.items():
            print(f"{clave}. {titulo}")
        print("0. Salir")
        opcion = input("Opcion: ")
        if opcion == "0":
            print("Hasta luego")
            return
        if opcion not in acciones:
            print("Opcion invalida")
            continue
        try:
            acciones[opcion][1](servicio)
        except ErrorSolicitud as error:
            print(f"Error: {error}")


def registrar(servicio):
    print("--- Registrar solicitud ---")
    legajo = input("Legajo: ")
    estudiante = servicio.obtener_estudiante(legajo)
    tipo = pedir_opcion("Tipo", Tipo, "tipo invalido")
    prioridad = pedir_opcion("Prioridad", Prioridad, "prioridad invalida")
    solicitud = servicio.registrar(NuevaSolicitud(legajo, tipo, prioridad, input("Descripcion: ")))
    print(f"Solicitud {solicitud.id} registrada para {estudiante.nombre}")
    print(f"Prioridad: {solicitud.prioridad.value} - Vence: {solicitud.vence}")


def cambiar_estado(servicio):
    print("--- Cambiar estado ---")
    numero = pedir_numero("Numero de solicitud: ")
    print(f"Estado actual: {servicio.obtener_solicitud(numero).estado.value}")
    nuevo = pedir_opcion("Nuevo estado", ESTADOS_DESTINO, "estado invalido")
    servicio.cambiar_estado(numero, nuevo)
    print(f"Estado actualizado a {nuevo.value}")


def asignar(servicio):
    print("--- Asignar responsable ---")
    numero = pedir_numero("Numero de solicitud: ")
    servicio.obtener_solicitud(numero)
    for responsable in servicio.responsables():
        print(f"{responsable.id} - {responsable.nombre} ({responsable.area})")
    responsable = servicio.asignar(numero, pedir_numero("Numero de responsable: "))
    print(f"Responsable asignado: {responsable.nombre}")


def buscar(servicio):
    print("--- Buscar solicitudes ---")
    print("1. Por estado")
    print("2. Por legajo")
    print("3. Todas")
    opcion = input("Opcion: ")
    if opcion == "1":
        encontradas = servicio.buscar(estado=input("Estado: "))
    elif opcion == "2":
        encontradas = servicio.buscar(legajo=input("Legajo: "))
    elif opcion == "3":
        encontradas = servicio.buscar()
    else:
        print("Opcion invalida")
        return
    for s in encontradas:
        print(
            f"#{s.id} | {s.legajo} | {s.tipo.value} | {s.prioridad.value}"
            f" | {s.estado.value} | vence {s.vence}"
        )
    print(f"Encontradas: {len(encontradas)}")


def reporte(servicio):
    print("--- Reporte general ---")
    for linea in servicio.reporte_general():
        print(linea)


def pedir_numero(pregunta):
    try:
        return int(input(pregunta))
    except ValueError:
        raise ErrorSolicitud("debe ingresar un numero") from None


def pedir_opcion(pregunta, opciones, error):
    valor = input(f"{pregunta} ({'/'.join(o.value for o in opciones)}): ")
    for opcion in opciones:
        if opcion.value == valor:
            return opcion
    raise ErrorSolicitud(error)
