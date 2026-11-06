# sistema de solicitudes academicas
from datetime import date

from gestion_solicitudes.modelos import ErrorSolicitud, Estado, NuevaSolicitud, Prioridad, Solicitud, Tipo
from gestion_solicitudes.repositorio import RepositorioJson

ARCHIVO_DATOS = "datos.json"
repositorio = None


def buscar_por(lista, atributo, valor, error):
    for elemento in lista:
        if getattr(elemento, atributo) == valor:
            return elemento
    raise ErrorSolicitud(error)


def imprimir_filas(lista):
    for s in lista:
        print(f"#{s.id} | {s.legajo} | {s.tipo.value} | {s.prioridad.value} | {s.estado.value} | vence {s.vence}")
    print(f"Encontradas: {len(lista)}")


def pedir_solicitud():
    numero = int(input("Numero de solicitud: "))
    return buscar_por(repositorio.solicitudes, "id", numero, "no existe la solicitud")


def pedir_opcion(pregunta, opciones, error):
    valor = input(f"{pregunta} ({'/'.join(o.value for o in opciones)}): ")
    for opcion in opciones:
        if opcion.value == valor:
            return opcion
    raise ErrorSolicitud(error)


def registrar():
    print("--- Registrar solicitud ---")
    legajo = input("Legajo: ")
    estudiante = buscar_por(repositorio.estudiantes, "legajo", legajo, "no existe el estudiante")
    tipo = pedir_opcion("Tipo", list(Tipo), "tipo invalido")
    prioridad = pedir_opcion("Prioridad", list(Prioridad), "prioridad invalida")
    nueva = NuevaSolicitud(legajo, tipo, prioridad, input("Descripcion: "))
    solicitud = Solicitud.crear(len(repositorio.solicitudes) + 1, nueva, date.today())
    repositorio.solicitudes.append(solicitud)
    repositorio.guardar()
    print(f"Solicitud {solicitud.id} registrada para {estudiante.nombre}")
    print(f"Prioridad: {solicitud.prioridad.value} - Vence: {solicitud.vence}")


def cambiar_estado():
    print("--- Cambiar estado ---")
    solicitud = pedir_solicitud()
    print(f"Estado actual: {solicitud.estado.value}")
    destinos = [Estado.EN_PROCESO, Estado.RESUELTA, Estado.RECHAZADA]
    nuevo = pedir_opcion("Nuevo estado", destinos, "estado invalido")
    solicitud.cambiar_estado(nuevo)
    repositorio.guardar()
    print(f"Estado actualizado a {nuevo.value}")


def asignar():
    print("--- Asignar responsable ---")
    solicitud = pedir_solicitud()
    for responsable in repositorio.responsables:
        print(f"{responsable.id} - {responsable.nombre} ({responsable.area})")
    numero = int(input("Numero de responsable: "))
    responsable = buscar_por(repositorio.responsables, "id", numero, "no existe el responsable")
    solicitud.asignar(responsable)
    repositorio.guardar()
    print(f"Responsable asignado: {responsable.nombre}")


def buscar():
    print("--- Buscar solicitudes ---")
    print("1. Por estado")
    print("2. Por legajo")
    print("3. Todas")
    opcion = input("Opcion: ")
    if opcion == "1":
        valor = input("Estado: ")
        imprimir_filas([s for s in repositorio.solicitudes if s.estado.value == valor])
    elif opcion == "2":
        valor = input("Legajo: ")
        imprimir_filas([s for s in repositorio.solicitudes if s.legajo == valor])
    elif opcion == "3":
        imprimir_filas(repositorio.solicitudes)
    else:
        print("Opcion invalida")


def contar_estado(estado):
    return len([s for s in repositorio.solicitudes if s.estado is estado])


def reporte():
    print("--- Reporte general ---")
    hoy = date.today()
    vencidas = [s for s in repositorio.solicitudes if s.esta_vencida(hoy)]
    print(f"Total: {len(repositorio.solicitudes)}")
    print(f"Pendientes: {contar_estado(Estado.PENDIENTE)}")
    print(f"En proceso: {contar_estado(Estado.EN_PROCESO)}")
    print(f"Resueltas: {contar_estado(Estado.RESUELTA)}")
    print(f"Rechazadas: {contar_estado(Estado.RECHAZADA)}")
    print(f"Vencidas: {len(vencidas)}")


def main():
    global repositorio
    repositorio = RepositorioJson(ARCHIVO_DATOS)
    while True:
        print("")
        print("=== Solicitudes Academicas ===")
        print("1. Registrar solicitud")
        print("2. Cambiar estado")
        print("3. Asignar responsable")
        print("4. Buscar solicitudes")
        print("5. Reporte general")
        print("0. Salir")
        opcion = input("Opcion: ")
        try:
            if opcion == "1":
                registrar()
            elif opcion == "2":
                cambiar_estado()
            elif opcion == "3":
                asignar()
            elif opcion == "4":
                buscar()
            elif opcion == "5":
                reporte()
            elif opcion == "0":
                print("Hasta luego")
                break
            else:
                print("Opcion invalida")
        except ErrorSolicitud as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
