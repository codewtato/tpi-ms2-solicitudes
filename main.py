# sistema de solicitudes academicas
import json
from dataclasses import asdict
from datetime import date, timedelta

from gestion_solicitudes.modelos import Estado, Estudiante, Prioridad, Responsable, Solicitud, Tipo

solicitudes = []
estudiantes = []
responsables = []
ARCHIVO_DATOS = "datos.json"
LARGO_MINIMO_DESCRIPCION = 10


def solicitud_desde_dict(datos):
    return Solicitud(
        datos["id"], datos["legajo"], Tipo(datos["tipo"]), Prioridad(datos["prioridad"]), datos["descripcion"],
        date.fromisoformat(datos["fecha"]), date.fromisoformat(datos["vence"]), Estado(datos["estado"]),
        datos["responsable"],
    )


def solicitud_a_dict(solicitud):
    return {
        **asdict(solicitud),
        "tipo": solicitud.tipo.value,
        "prioridad": solicitud.prioridad.value,
        "fecha": solicitud.fecha.isoformat(),
        "vence": solicitud.vence.isoformat(),
        "estado": solicitud.estado.value,
    }


def cargar():
    global solicitudes, estudiantes, responsables
    try:
        f = open(ARCHIVO_DATOS)
        d = json.load(f)
        f.close()
        solicitudes = [solicitud_desde_dict(s) for s in d["solicitudes"]]
        estudiantes = [Estudiante(**e) for e in d["estudiantes"]]
        responsables = [Responsable(**r) for r in d["responsables"]]
    except:
        # si no se puede leer arrancamos con los datos de ejemplo
        estudiantes = [Estudiante("1001", "Ana Prueba"), Estudiante("1002", "Bruno Ejemplo")]
        responsables = [Responsable(1, "Diego Bedel", "Bedelia"), Responsable(2, "Elena Secretaria", "Secretaria")]
        solicitudes = []


def guardar():
    f = open(ARCHIVO_DATOS, "w")
    json.dump(
        {
            "solicitudes": [solicitud_a_dict(s) for s in solicitudes],
            "estudiantes": [asdict(e) for e in estudiantes],
            "responsables": [asdict(r) for r in responsables],
        },
        f,
        indent=2,
    )
    f.close()


def crear_solicitud(id, legajo, tipo, prioridad, descripcion, fecha, vence, estado, responsable):
    return Solicitud(id, legajo, tipo, prioridad, descripcion, fecha, vence, estado, responsable)


def buscar_por(lista, atributo, valor):
    for elemento in lista:
        if getattr(elemento, atributo) == valor:
            return elemento
    return None


def calcular_plazo(tipo):
    if tipo is Tipo.CERTIFICADO:
        return 5
    if tipo is Tipo.EQUIVALENCIA:
        return 30
    return 7


def calcular_area(tipo):
    return "Bedelia" if tipo is Tipo.CERTIFICADO else "Secretaria"


def esta_abierta(solicitud):
    return solicitud.estado in (Estado.PENDIENTE, Estado.EN_PROCESO)


def transicion_permitida(actual, nuevo):
    if actual is Estado.PENDIENTE:
        return nuevo in (Estado.EN_PROCESO, Estado.RECHAZADA)
    return nuevo in (Estado.RESUELTA, Estado.RECHAZADA)


def imprimir_filas(lista):
    for s in lista:
        print(f"#{s.id} | {s.legajo} | {s.tipo.value} | {s.prioridad.value} | {s.estado.value} | vence {s.vence}")
    print(f"Encontradas: {len(lista)}")


def pedir_solicitud():
    solicitud = buscar_por(solicitudes, "id", int(input("Numero de solicitud: ")))
    if solicitud is None:
        print("Error: no existe la solicitud")
    return solicitud


def pedir_datos_nueva_solicitud():
    try:
        tipo = Tipo(input("Tipo (certificado/equivalencia/reclamo): "))
    except ValueError:
        print("Error: tipo invalido")
        return None
    try:
        prioridad = Prioridad(input("Prioridad (alta/media/baja): "))
    except ValueError:
        print("Error: prioridad invalida")
        return None
    descripcion = input("Descripcion: ")
    if len(descripcion) < LARGO_MINIMO_DESCRIPCION:
        print("Error: la descripcion debe tener al menos 10 caracteres")
        return None
    return tipo, prioridad, descripcion


def registrar():
    print("--- Registrar solicitud ---")
    legajo = input("Legajo: ")
    estudiante = buscar_por(estudiantes, "legajo", legajo)
    if estudiante is None:
        print("Error: no existe el estudiante")
        return
    datos = pedir_datos_nueva_solicitud()
    if datos is None:
        return
    tipo, prioridad, descripcion = datos
    if tipo is Tipo.RECLAMO:  # los reclamos siempre son prioridad alta
        prioridad = Prioridad.ALTA
    hoy = date.today()
    solicitud = crear_solicitud(len(solicitudes) + 1, legajo, tipo, prioridad, descripcion, hoy,
                                hoy + timedelta(days=calcular_plazo(tipo)), Estado.PENDIENTE, None)
    solicitudes.append(solicitud)
    guardar()
    print(f"Solicitud {solicitud.id} registrada para {estudiante.nombre}")
    print(f"Prioridad: {solicitud.prioridad.value} - Vence: {solicitud.vence}")


def cambiar_estado():
    print("--- Cambiar estado ---")
    solicitud = pedir_solicitud()
    if solicitud is None:
        return
    print(f"Estado actual: {solicitud.estado.value}")
    valor = input("Nuevo estado (en_proceso/resuelta/rechazada): ")
    if valor not in ("en_proceso", "resuelta", "rechazada"):
        print("Error: estado invalido")
        return
    nuevo = Estado(valor)
    if not esta_abierta(solicitud):
        print("Error: la solicitud ya esta cerrada")
    elif not transicion_permitida(solicitud.estado, nuevo):
        print(f"Error: no se puede pasar de {solicitud.estado.value} a {nuevo.value}")
    elif nuevo is Estado.RESUELTA and solicitud.responsable is None:
        print("Error: no se puede resolver sin responsable")
    else:
        solicitud.estado = nuevo
        guardar()
        print(f"Estado actualizado a {nuevo.value}")


def asignar():
    print("--- Asignar responsable ---")
    solicitud = pedir_solicitud()
    if solicitud is None:
        return
    for responsable in responsables:
        print(f"{responsable.id} - {responsable.nombre} ({responsable.area})")
    responsable = buscar_por(responsables, "id", int(input("Numero de responsable: ")))
    area = calcular_area(solicitud.tipo)
    if responsable is None:
        print("Error: no existe el responsable")
    elif responsable.area != area:
        print(f"Error: ese tipo lo atiende {area}")
    else:
        solicitud.responsable = responsable.id
        solicitud.estado = Estado.EN_PROCESO
        guardar()
        print(f"Responsable asignado: {responsable.nombre}")


def buscar():
    print("--- Buscar solicitudes ---")
    print("1. Por estado")
    print("2. Por legajo")
    print("3. Todas")
    opcion = input("Opcion: ")
    if opcion == "1":
        valor = input("Estado: ")
        imprimir_filas([s for s in solicitudes if s.estado.value == valor])
    elif opcion == "2":
        valor = input("Legajo: ")
        imprimir_filas([s for s in solicitudes if s.legajo == valor])
    elif opcion == "3":
        imprimir_filas(solicitudes)
    else:
        print("Opcion invalida")


def contar_estado(estado):
    return len([s for s in solicitudes if s.estado is estado])


def reporte():
    print("--- Reporte general ---")
    hoy = date.today()
    vencidas = [s for s in solicitudes if esta_abierta(s) and s.vence <= hoy]
    print(f"Total: {len(solicitudes)}")
    print(f"Pendientes: {contar_estado(Estado.PENDIENTE)}")
    print(f"En proceso: {contar_estado(Estado.EN_PROCESO)}")
    print(f"Resueltas: {contar_estado(Estado.RESUELTA)}")
    print(f"Rechazadas: {contar_estado(Estado.RECHAZADA)}")
    print(f"Vencidas: {len(vencidas)}")


def main():
    cargar()
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


if __name__ == "__main__":
    main()
