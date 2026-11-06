# sistema de solicitudes academicas
import json
from datetime import datetime, timedelta

solicitudes = []
estudiantes = []
responsables = []
ARCHIVO_DATOS = "datos.json"
LARGO_MINIMO_DESCRIPCION = 10


def cargar():
    global solicitudes, estudiantes, responsables
    try:
        f = open(ARCHIVO_DATOS)
        d = json.load(f)
        f.close()
        solicitudes = d["solicitudes"]
        estudiantes = d["estudiantes"]
        responsables = d["responsables"]
    except:
        # si no se puede leer arrancamos con los datos de ejemplo
        estudiantes = [
            {"legajo": "1001", "nombre": "Ana Prueba"},
            {"legajo": "1002", "nombre": "Bruno Ejemplo"},
        ]
        responsables = [
            {"id": 1, "nombre": "Diego Bedel", "area": "Bedelia"},
            {"id": 2, "nombre": "Elena Secretaria", "area": "Secretaria"},
        ]
        solicitudes = []


def guardar():
    f = open(ARCHIVO_DATOS, "w")
    json.dump({"solicitudes": solicitudes, "estudiantes": estudiantes, "responsables": responsables}, f, indent=2)
    f.close()


def crear_solicitud(id, legajo, tipo, prioridad, descripcion, fecha, vence, estado, responsable):
    return {"id": id, "legajo": legajo, "tipo": tipo, "prioridad": prioridad, "descripcion": descripcion,
            "fecha": fecha, "vence": vence, "estado": estado, "responsable": responsable}


def buscar_por(lista, clave, valor):
    for elemento in lista:
        if elemento[clave] == valor:
            return elemento
    return None


def calcular_plazo(tipo):
    if tipo == "certificado":
        return 5
    if tipo == "equivalencia":
        return 30
    return 7


def calcular_area(tipo):
    return "Bedelia" if tipo == "certificado" else "Secretaria"


def esta_abierta(solicitud):
    return solicitud["estado"] in ("pendiente", "en_proceso")


def transicion_permitida(actual, nuevo):
    if actual == "pendiente":
        return nuevo in ("en_proceso", "rechazada")
    return nuevo in ("resuelta", "rechazada")


def imprimir_filas(lista):
    for s in lista:
        print("#" + str(s["id"]) + " | " + s["legajo"] + " | " + s["tipo"] + " | " + s["prioridad"]
              + " | " + s["estado"] + " | vence " + s["vence"])
    print("Encontradas: " + str(len(lista)))


def pedir_solicitud():
    solicitud = buscar_por(solicitudes, "id", int(input("Numero de solicitud: ")))
    if solicitud is None:
        print("Error: no existe la solicitud")
    return solicitud


def pedir_datos_nueva_solicitud():
    tipo = input("Tipo (certificado/equivalencia/reclamo): ")
    if tipo not in ("certificado", "equivalencia", "reclamo"):
        print("Error: tipo invalido")
        return None
    prioridad = input("Prioridad (alta/media/baja): ")
    if prioridad not in ("alta", "media", "baja"):
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
    if tipo == "reclamo":  # los reclamos siempre son prioridad alta
        prioridad = "alta"
    hoy = datetime.now()
    vence = hoy + timedelta(days=calcular_plazo(tipo))
    solicitud = crear_solicitud(len(solicitudes) + 1, legajo, tipo, prioridad, descripcion,
                                hoy.strftime("%Y-%m-%d"), vence.strftime("%Y-%m-%d"), "pendiente", None)
    solicitudes.append(solicitud)
    guardar()
    print("Solicitud " + str(solicitud["id"]) + " registrada para " + estudiante["nombre"])
    print("Prioridad: " + solicitud["prioridad"] + " - Vence: " + solicitud["vence"])


def cambiar_estado():
    print("--- Cambiar estado ---")
    solicitud = pedir_solicitud()
    if solicitud is None:
        return
    print("Estado actual: " + solicitud["estado"])
    nuevo = input("Nuevo estado (en_proceso/resuelta/rechazada): ")
    if nuevo not in ("en_proceso", "resuelta", "rechazada"):
        print("Error: estado invalido")
    elif not esta_abierta(solicitud):
        print("Error: la solicitud ya esta cerrada")
    elif not transicion_permitida(solicitud["estado"], nuevo):
        print("Error: no se puede pasar de " + solicitud["estado"] + " a " + nuevo)
    elif nuevo == "resuelta" and solicitud["responsable"] is None:
        print("Error: no se puede resolver sin responsable")
    else:
        solicitud["estado"] = nuevo
        guardar()
        print("Estado actualizado a " + nuevo)


def asignar():
    print("--- Asignar responsable ---")
    solicitud = pedir_solicitud()
    if solicitud is None:
        return
    for responsable in responsables:
        print(str(responsable["id"]) + " - " + responsable["nombre"] + " (" + responsable["area"] + ")")
    responsable = buscar_por(responsables, "id", int(input("Numero de responsable: ")))
    area = calcular_area(solicitud["tipo"])
    if responsable is None:
        print("Error: no existe el responsable")
    elif responsable["area"] != area:
        print("Error: ese tipo lo atiende " + area)
    else:
        solicitud["responsable"] = responsable["id"]
        solicitud["estado"] = "en_proceso"
        guardar()
        print("Responsable asignado: " + responsable["nombre"])


def buscar():
    print("--- Buscar solicitudes ---")
    print("1. Por estado")
    print("2. Por legajo")
    print("3. Todas")
    opcion = input("Opcion: ")
    if opcion == "1":
        valor = input("Estado: ")
        imprimir_filas([s for s in solicitudes if s["estado"] == valor])
    elif opcion == "2":
        valor = input("Legajo: ")
        imprimir_filas([s for s in solicitudes if s["legajo"] == valor])
    elif opcion == "3":
        imprimir_filas(solicitudes)
    else:
        print("Opcion invalida")


def contar_estado(estado):
    return len([s for s in solicitudes if s["estado"] == estado])


def reporte():
    print("--- Reporte general ---")
    ahora = datetime.now()
    vencidas = [s for s in solicitudes
                if esta_abierta(s) and datetime.strptime(s["vence"], "%Y-%m-%d") < ahora]
    print("Total: " + str(len(solicitudes)))
    print("Pendientes: " + str(contar_estado("pendiente")))
    print("En proceso: " + str(contar_estado("en_proceso")))
    print("Resueltas: " + str(contar_estado("resuelta")))
    print("Rechazadas: " + str(contar_estado("rechazada")))
    print("Vencidas: " + str(len(vencidas)))


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
