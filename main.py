# sistema de solicitudes academicas
import json
from datetime import datetime, timedelta

# variables globales
solicitudes = []
estudiantes = []
responsables = []
ARCH = "datos.json"


def cargar():
    global solicitudes, estudiantes, responsables
    try:
        f = open(ARCH)
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
    f = open(ARCH, "w")
    json.dump({"solicitudes": solicitudes, "estudiantes": estudiantes, "responsables": responsables}, f, indent=2)
    f.close()


def crear_solicitud(id, legajo, tipo, prioridad, descripcion, fecha, vence, estado, responsable):
    return {"id": id, "legajo": legajo, "tipo": tipo, "prioridad": prioridad, "descripcion": descripcion,
            "fecha": fecha, "vence": vence, "estado": estado, "responsable": responsable}


def registrar():
    print("--- Registrar solicitud ---")
    leg = input("Legajo: ")
    est = None
    for e in estudiantes:
        if e["legajo"] == leg:
            est = e
    if est == None:
        print("Error: no existe el estudiante")
        return
    t = input("Tipo (certificado/equivalencia/reclamo): ")
    if t != "certificado" and t != "equivalencia" and t != "reclamo":
        print("Error: tipo invalido")
        return
    p = input("Prioridad (alta/media/baja): ")
    if p != "alta" and p != "media" and p != "baja":
        print("Error: prioridad invalida")
        return
    desc = input("Descripcion: ")
    if len(desc) < 10:
        print("Error: la descripcion debe tener al menos 10 caracteres")
        return
    # calculo el plazo segun el tipo
    hoy = datetime.now()
    if t == "certificado":
        plazo = 5
    elif t == "equivalencia":
        plazo = 30
    else:
        plazo = 7
    # los reclamos siempre son prioridad alta
    if t == "reclamo":
        p = "alta"
    vence = hoy + timedelta(days=plazo)
    s = crear_solicitud(len(solicitudes) + 1, leg, t, p, desc, hoy.strftime("%Y-%m-%d"),
                        vence.strftime("%Y-%m-%d"), "pendiente", None)
    solicitudes.append(s)
    guardar()
    print("Solicitud " + str(s["id"]) + " registrada para " + est["nombre"])
    print("Prioridad: " + s["prioridad"] + " - Vence: " + s["vence"])


def cambiar_estado():
    print("--- Cambiar estado ---")
    n = int(input("Numero de solicitud: "))
    s = None
    for x in solicitudes:
        if x["id"] == n:
            s = x
    if s == None:
        print("Error: no existe la solicitud")
        return
    print("Estado actual: " + s["estado"])
    nuevo = input("Nuevo estado (en_proceso/resuelta/rechazada): ")
    if nuevo != "en_proceso" and nuevo != "resuelta" and nuevo != "rechazada":
        print("Error: estado invalido")
        return
    if s["estado"] == "pendiente":
        if nuevo != "en_proceso" and nuevo != "rechazada":
            print("Error: no se puede pasar de " + s["estado"] + " a " + nuevo)
            return
    elif s["estado"] == "en_proceso":
        if nuevo != "resuelta" and nuevo != "rechazada":
            print("Error: no se puede pasar de " + s["estado"] + " a " + nuevo)
            return
    else:
        print("Error: la solicitud ya esta cerrada")
        return
    if nuevo == "resuelta" and s["responsable"] == None:
        print("Error: no se puede resolver sin responsable")
        return
    s["estado"] = nuevo
    guardar()
    print("Estado actualizado a " + nuevo)


def asignar():
    print("--- Asignar responsable ---")
    n = int(input("Numero de solicitud: "))
    s = None
    for x in solicitudes:
        if x["id"] == n:
            s = x
    if s == None:
        print("Error: no existe la solicitud")
        return
    for r in responsables:
        print(str(r["id"]) + " - " + r["nombre"] + " (" + r["area"] + ")")
    rid = int(input("Numero de responsable: "))
    r = None
    for x in responsables:
        if x["id"] == rid:
            r = x
    if r == None:
        print("Error: no existe el responsable")
        return
    # cada tipo lo atiende un area
    if s["tipo"] == "certificado":
        area = "Bedelia"
    else:
        area = "Secretaria"
    if r["area"] != area:
        print("Error: ese tipo lo atiende " + area)
        return
    s["responsable"] = r["id"]
    # al asignar pasa a en proceso
    s["estado"] = "en_proceso"
    guardar()
    print("Responsable asignado: " + r["nombre"])


def buscar():
    print("--- Buscar solicitudes ---")
    print("1. Por estado")
    print("2. Por legajo")
    print("3. Todas")
    op = input("Opcion: ")
    c = 0
    if op == "1":
        v = input("Estado: ")
        for s in solicitudes:
            if s["estado"] == v:
                print("#" + str(s["id"]) + " | " + s["legajo"] + " | " + s["tipo"] + " | " + s["prioridad"] + " | " + s["estado"] + " | vence " + s["vence"])
                c = c + 1
    elif op == "2":
        v = input("Legajo: ")
        for s in solicitudes:
            if s["legajo"] == v:
                print("#" + str(s["id"]) + " | " + s["legajo"] + " | " + s["tipo"] + " | " + s["prioridad"] + " | " + s["estado"] + " | vence " + s["vence"])
                c = c + 1
    elif op == "3":
        for s in solicitudes:
            print("#" + str(s["id"]) + " | " + s["legajo"] + " | " + s["tipo"] + " | " + s["prioridad"] + " | " + s["estado"] + " | vence " + s["vence"])
            c = c + 1
    else:
        print("Opcion invalida")
        return
    print("Encontradas: " + str(c))


def reporte():
    print("--- Reporte general ---")
    a = 0
    b = 0
    c = 0
    d = 0
    v = 0
    hoy = datetime.now()
    for s in solicitudes:
        if s["estado"] == "pendiente":
            a = a + 1
        elif s["estado"] == "en_proceso":
            b = b + 1
        elif s["estado"] == "resuelta":
            c = c + 1
        else:
            d = d + 1
        if s["estado"] == "pendiente" or s["estado"] == "en_proceso":
            if datetime.strptime(s["vence"], "%Y-%m-%d") < hoy:
                v = v + 1
    print("Total: " + str(len(solicitudes)))
    print("Pendientes: " + str(a))
    print("En proceso: " + str(b))
    print("Resueltas: " + str(c))
    print("Rechazadas: " + str(d))
    print("Vencidas: " + str(v))


# ya no se usa, lo dejo por las dudas
def calcular_total_viejo():
    t = 0
    for s in solicitudes:
        t = t + 1
    return t


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
        o = input("Opcion: ")
        if o == "1":
            registrar()
        elif o == "2":
            cambiar_estado()
        elif o == "3":
            asignar()
        elif o == "4":
            buscar()
        elif o == "5":
            reporte()
        elif o == "0":
            print("Hasta luego")
            break
        else:
            print("Opcion invalida")


main()
