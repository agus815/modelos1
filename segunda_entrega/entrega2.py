def importar():
    n = 0
    incompatibles = {}
    tiempo_individual = {}

    f = open("problema2.txt", "r")
    for linea in f:
        linea_split = linea.split()
        if linea_split[0] == "p":
            n = int(linea_split[2])
            e = int(linea_split[3])
            for i in range(1, n + 1):
                incompatibles[i] = []
        elif linea_split[0] == "e":
            incompatibles[int(linea_split[1])].append(int(linea_split[2]))
            incompatibles[int(linea_split[2])].append(int(linea_split[1]))
        elif linea_split[0] == "n":
            tiempo_individual[int(linea_split[1])] = int(linea_split[2])
    f.close()
    return incompatibles, tiempo_individual, n


def es_compatible(prenda, prendas_a_comparar, incompatibles):
    # Determina si una prenda es compatible con una lista de prendas
    for p in prendas_a_comparar:
        if p in incompatibles[prenda]:
            return False
    return True


def compatibles(prenda, incompatibles, n):
    # Obtiene todas las prendas compatibles con una
    compatibles = []
    for p in range(1, n + 1):
        if (p != prenda) and (p not in incompatibles[prenda]):
            compatibles.append(p)
    return compatibles


def interseccion(comp, prendas_no_lavadas):
    # Obtiene la interseccion entre dos listas de prendas
    lista = []
    for i in range(len(comp)):
        if comp[i] in prendas_no_lavadas:
            lista.append(comp[i])
    return lista


def p_mas_incompatibilidades_y_tardanza(prendas, incompatibilidades, t_individuales):
    # Obtiene de una lista de prendas la que más tarda, si hay dos que tardan lo mismo obtiene
    # la que más incompatibilidades tiene
    t_max = 0
    max_incomp = 0
    prenda_a_lavar = None

    for p in prendas:
        if (t_individuales[p] > t_max) or ((t_individuales[p] == t_max) and (len(incompatibilidades[p]) > max_incomp)):
            max_incomp = len(incompatibilidades[p])
            t_max = t_individuales[p]
            prenda_a_lavar = p

    return prenda_a_lavar


def solucion_optima():
    # ALgoritmo de la solucion propuesta

    incompatibilidades, t_individuales, n = importar()
    prendas_no_lavadas = []
    combinaciones = []

    for i in range(1, n + 1):
        prendas_no_lavadas.append(i)

    while len(prendas_no_lavadas) != 0:
        prox_a_lavar = p_mas_incompatibilidades_y_tardanza(prendas_no_lavadas, incompatibilidades, t_individuales)

        prendas_no_lavadas.remove(prox_a_lavar)
        prendas_a_lavar = [prox_a_lavar]

        comp = compatibles(prox_a_lavar, incompatibilidades, n)
        compatibles_a_usar = interseccion(comp, prendas_no_lavadas)

        while compatibles_a_usar:
            prox_prenda = p_mas_incompatibilidades_y_tardanza(compatibles_a_usar, incompatibilidades, t_individuales)

            if es_compatible(prox_prenda, prendas_a_lavar, incompatibilidades):
                prendas_a_lavar.append(prox_prenda)
                prendas_no_lavadas.remove(prox_prenda)

            compatibles_a_usar.remove(prox_prenda)

        combinaciones.append(prendas_a_lavar)

    return combinaciones
