from io import StringIO
import copy


def eliminarEspacios(Lista):
    return [o.strip() for o in Lista if o.strip()]

def BitsParaCadaRed(lista_con_nombres_y_hosts):
    ListaDeDiccionarios = []
    for subred in lista_con_nombres_y_hosts:
        hosts = subred["hosts"]
        nombre = subred["nombre"]

        bits = 1
        while (2 ** bits) - 2 < hosts:
            bits += 1

        diccionario = {
            "nombre": nombre,
            "hostRequeridos": hosts,
            "bitsNecesarios": bits,
            "numeroDeHostsMaximos": (2 ** bits) - 2,
            "mascara": 32 - bits
        }

        ListaDeDiccionarios.append(diccionario)
    return ListaDeDiccionarios


def IpEnBinario(IpBase):
    partes = [int(p) for p in IpBase.split(".")]
    return ".".join([bin(o)[2:].zfill(8) for o in partes])

def IpEnEntero(IpBase):
    partes = [int(p) for p in IpBase.split(".")]
    return (partes[0] << 24) + (partes[1] << 16) + (partes[2] << 8) + partes[3]

def enteroAIp(entero):
    return "{}.{}.{}.{}".format(
        (entero >> 24) & 255,
        (entero >> 16) & 255,
        (entero >> 8) & 255,
        entero & 255
    )

def ya_cabe_una_subred(mascara_actual, bits_necesarios):
    return (32 - mascara_actual) >= bits_necesarios

def asignar_esa_subred(ip_entero, mascara_actual, subred):
    tamanio = 2 ** (32 - mascara_actual)
    subred["ipRed"] = enteroAIp(ip_entero)
    subred["ipPrimera"] = enteroAIp(ip_entero + 1)
    subred["ipUltima"] = enteroAIp(ip_entero + tamanio - 2)
    subred["ipBroadcast"] = enteroAIp(ip_entero + tamanio - 1)
    subred["mascara"] = mascara_actual

def imprimir_en_pdf(ip_entero, mascara, nivel,nombre=None):
    ip_str = enteroAIp(ip_entero)
    linea = ("   " * nivel) + f"{ip_str}/{mascara}"
    if nombre:
        linea += f" → {nombre}"
    print(linea)

def construir_arbol(ip_entero, mascara_actual, subredes_por_asignar, nivel):
    if not subredes_por_asignar:
        return

    

    if ya_cabe_una_subred(mascara_actual, subredes_por_asignar[0]["bitsNecesarios"]):
        if (32 - mascara_actual) == subredes_por_asignar[0]["bitsNecesarios"]:
            imprimir_en_pdf(ip_entero, mascara_actual, nivel, subredes_por_asignar[0]["nombre"])
            asignar_esa_subred(ip_entero, mascara_actual, subredes_por_asignar[0])
            subredes_por_asignar.pop(0)
            return
    imprimir_en_pdf(ip_entero, mascara_actual, nivel)

    mitad = 2 ** (32 - (mascara_actual + 1))
    construir_arbol(ip_entero, mascara_actual + 1, subredes_por_asignar, nivel + 1)
    construir_arbol(ip_entero + mitad, mascara_actual + 1, subredes_por_asignar, nivel + 1)



def procesar_entrada_vlsm(ip_base_con_mascara, texto_hosts):
    IpBase = ip_base_con_mascara.split("/")[0]
    Mascara = int(ip_base_con_mascara.split("/")[1])

    # Procesar entrada tipo: LAN-A:50, LAN-B:30, WAN-1:2
    lista_raw = texto_hosts.split(",")
    subredes = []
    for item in lista_raw:
        nombre, cantidad = item.split(":")
        subredes.append({
            "nombre": nombre.strip(),
            "hosts": int(cantidad.strip())
        })

    # Ordenamos de mayor a menor
    subredes.sort(key=lambda x: x["hosts"], reverse=True)

    # Convertimos a estructuras con bits y máscara
    lista_final = []
    for s in subredes:
        bits = 1
        while (2 ** bits) - 2 < s["hosts"]:
            bits += 1
        lista_final.append({
            "nombre": s["nombre"],
            "hostRequeridos": s["hosts"],
            "bitsNecesarios": bits,
            "numeroDeHostsMaximos": (2 ** bits) - 2,
            "mascara": 32 - bits
        })

    # Construimos el árbol
    ip_base_entero = IpEnEntero(IpBase)
    copia = copy.deepcopy(lista_final)

    # Capturamos la salida como string (en lugar de print directo)
    salida = StringIO()

    def imprimir_arbol(ip_entero, mascara_actual, subredes_por_asignar, nivel):
        if not subredes_por_asignar:
            return

        if ya_cabe_una_subred(mascara_actual, subredes_por_asignar[0]["bitsNecesarios"]):
            if (32 - mascara_actual) == subredes_por_asignar[0]["bitsNecesarios"]:
                nombre = subredes_por_asignar[0]["nombre"]
                linea = ("   " * nivel) + f"{enteroAIp(ip_entero)}/{mascara_actual} → {nombre}"
                print(linea, file=salida)
                asignar_esa_subred(ip_entero, mascara_actual, subredes_por_asignar[0])
                subredes_por_asignar.pop(0)
                return

        linea = ("   " * nivel) + f"{enteroAIp(ip_entero)}/{mascara_actual}"
        print(linea, file=salida)

        mitad = 2 ** (32 - (mascara_actual + 1))
        imprimir_arbol(ip_entero, mascara_actual + 1, subredes_por_asignar, nivel + 1)
        imprimir_arbol(ip_entero + mitad, mascara_actual + 1, subredes_por_asignar, nivel + 1)

    imprimir_arbol(ip_base_entero, Mascara, copia, 0)

    arbol_str = salida.getvalue()
    # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    ListaDeBits = BitsParaCadaRed(subredes)

    # Primero imprimimos los resultados de las subredes calculadas
    for i, valor in enumerate(ListaDeBits):
        print(f"Red {valor['nombre']}:")
        print(f"  Hosts requeridos: {valor['hostRequeridos']}")
        print(f"  Bits necesarios: {valor['bitsNecesarios']}")
        print(f"  Número de hosts máximos: {valor['numeroDeHostsMaximos']}")
        print(f"  Máscara de subred: /{valor['mascara']}")
        print()

    print("Construyendo el árbol de subredes...")
    ip_base_entero = IpEnEntero(IpBase)

    subredes_copia = copy.deepcopy(ListaDeBits)  # Mantener los datos originales
    construir_arbol(ip_base_entero, Mascara, subredes_copia, 0)
    print("Árbol de subredes construido.")
    print("-----------------------------------"*5)

    # Convertimos la IP base a entero para calcular las subredes
    ip_actual = IpEnEntero(IpBase)
    ip_actual2 = IpEnEntero(IpBase)

    # Aquí va la validación del espacio disponible para cada subred
    MascaraFff = 32 - Mascara
    for subred in ListaDeBits:
        tamanio = 2 ** subred["bitsNecesarios"]
        
        # Validamos si la subred cabe dentro del espacio restante de la red base
        print(ip_actual +tamanio)
        print(ip_actual2 + 2**MascaraFff)
        if ip_actual + tamanio <= ip_actual2 + 2**MascaraFff:  # Verifica que no sobrepasemos el rango de IPs disponibles
            # Asignamos la dirección IP a la subred
            subred["ipRed"] = enteroAIp(ip_actual)
            subred["ipPrimera"] = enteroAIp(ip_actual + 1)
            subred["ipUltima"] = enteroAIp(ip_actual + tamanio - 2)
            subred["ipBroadcast"] = enteroAIp(ip_actual + tamanio - 1)

            # Avanzamos a la siguiente subred
            ip_actual += tamanio  # Incrementamos el puntero para la siguiente subred
        else:
            # Si no cabe, marcamos la subred como "No asignada"
            subred["ipRed"] = subred["ipPrimera"] = subred["ipUltima"] = subred["ipBroadcast"] = "No asignado"
            print(f"  {subred['nombre']} no puede ser asignada por falta de espacio.")

        # Mostramos la información de cada subred
        print(f"Subred {subred['nombre']}:")
        print(f"  IP de red: {subred['ipRed']}")
        print(f"  Primera IP: {subred['ipPrimera']}")
        print(f"  Última IP: {subred['ipUltima']}")
        print(f"  IP de broadcast: {subred['ipBroadcast']}")
        print(f"  Máscara de subred: /{subred['mascara']}")
        print()



    return {
        "arbol": arbol_str,
        "subredes": ListaDeBits
    }






# ======================= MAIN =======================

if __name__ == "__main__":
    import copy

    print(ya_cabe_una_subred(24, 6))  # True
    print(ya_cabe_una_subred(28, 6))  # False

    IpCompleta = input("Ingrese la Ip de esta forma, de esta no de otra forma EJEMPLO (192.168.0.0/24)  Ip: ")
    Mascara = int(IpCompleta.split("/")[1])
    IpBase = IpCompleta.split("/")[0]

    print("La IP en binario es: ", IpEnBinario(IpBase))
    print("La mascara es: ", Mascara)

    ListaDeHostsEnStr = input("Ingrese los nombres y hosts así: LAN-A:50, LAN-B:30, WAN-1:2 ...\n→ ")
    ListaDeHosts = ListaDeHostsEnStr.split(",")
    ListaDeHostsLimpia = eliminarEspacios(ListaDeHosts)

    listadesubredes = []
    for item in ListaDeHostsLimpia:
        nombre, host = item.split(":")
        listadesubredes.append({
            "nombre": nombre.strip(),
            "hosts": int(host.strip())
        })

    # Ordenar de mayor a menor según hosts
    listadesubredes.sort(key=lambda x: x["hosts"], reverse=True)
    '''ListaDeHostEnArreglo = eliminarEspacios(ListaDeHosts)
    listaDeHostEnArreglo = [int(host) for host in ListaDeHostEnArreglo]
    listaDeHostEnArreglo.sort(reverse=True)'''

    print("Los hosts son: ", ListaDeHostsLimpia)
    

   
    

    # Calcular los bits necesarios para cada subred
    ListaDeBits = BitsParaCadaRed(listadesubredes)

    # Primero imprimimos los resultados de las subredes calculadas
    for i, valor in enumerate(ListaDeBits):
        print(f"Red {valor['nombre']}:")
        print(f"  Hosts requeridos: {valor['hostRequeridos']}")
        print(f"  Bits necesarios: {valor['bitsNecesarios']}")
        print(f"  Número de hosts máximos: {valor['numeroDeHostsMaximos']}")
        print(f"  Máscara de subred: /{valor['mascara']}")
        print()

    print("Construyendo el árbol de subredes...")
    ip_base_entero = IpEnEntero(IpBase)

    subredes_copia = copy.deepcopy(ListaDeBits)  # Mantener los datos originales
    construir_arbol(ip_base_entero, Mascara, subredes_copia, 0)
    print("Árbol de subredes construido.")
    print("-----------------------------------"*5)

    # Convertimos la IP base a entero para calcular las subredes
    ip_actual = IpEnEntero(IpBase)
    ip_actual2 = IpEnEntero(IpBase)

    # Aquí va la validación del espacio disponible para cada subred
    MascaraFff = 32 - Mascara
    for subred in ListaDeBits:
        tamanio = 2 ** subred["bitsNecesarios"]
        
        # Validamos si la subred cabe dentro del espacio restante de la red base
        print(ip_actual +tamanio)
        print(ip_actual2 + 2**MascaraFff)
        if ip_actual + tamanio <= ip_actual2 + 2**MascaraFff:  # Verifica que no sobrepasemos el rango de IPs disponibles
            # Asignamos la dirección IP a la subred
            subred["ipRed"] = enteroAIp(ip_actual)
            subred["ipPrimera"] = enteroAIp(ip_actual + 1)
            subred["ipUltima"] = enteroAIp(ip_actual + tamanio - 2)
            subred["ipBroadcast"] = enteroAIp(ip_actual + tamanio - 1)

            # Avanzamos a la siguiente subred
            ip_actual += tamanio  # Incrementamos el puntero para la siguiente subred
        else:
            # Si no cabe, marcamos la subred como "No asignada"
            subred["ipRed"] = subred["ipPrimera"] = subred["ipUltima"] = subred["ipBroadcast"] = "No asignado"
            print(f"  {subred['nombre']} no puede ser asignada por falta de espacio.")

        # Mostramos la información de cada subred
        print(f"Subred {subred['nombre']}:")
        print(f"  IP de red: {subred['ipRed']}")
        print(f"  Primera IP: {subred['ipPrimera']}")
        print(f"  Última IP: {subred['ipUltima']}")
        print(f"  IP de broadcast: {subred['ipBroadcast']}")
        print(f"  Máscara de subred: /{subred['mascara']}")
        print()
