def importar():
    n = 0
    incompatibles = {}
    tiempo_individual = {}

    f = open("problema3.txt", "r")
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


def proponer_sol_lineal():
    incompatibles, tiempo_individual, n = importar()
    with open("problema1.mod", "w") as f:
        # declarar los tiempos iniciales de lavado:
        for i in range(1, 10):
            f.write(f"var I{i} >= 0;\n")

        # declarar tiempos finales de lavado
        for i in range(1, 10):
            f.write(f"var F{i} >= 0;\n")

        # declarar tiempo de cada lavadp
        for i in range(1, 10):
            f.write(f"var T{i} >= 0;\n")

        # declarar la variable del tiempo final
        f.write(f"var T_FINAL >= 0;\n")

        # declarar si se realiza el lavado i antes que j
        for i in range(1, 10):
            for j in range(1, 10):
                if i == j:
                    continue
                f.write(f"var YL{i}{j}, binary;\n")

        # declarar si en el lavado i se lava la prenda j
        for i in range(1, 10):
            for j in range(1, n + 1):
                f.write(f"var YP{i}{j}, binary;\n")

        # RESTRICCIONES
        # declaro la relacion entre el tiempo inicial y tiempo final de cada lavado
        for i in range(1, 10):
            f.write(f"s.t. REL_INI_FIN_{i}: I{i} + T{i} - F{i} = 0;\n")

        # evito superposicion entre los tiempos de lavado
        m_mayuscula = 200
        for i in range(1, 10):
            for j in range(i, 10):
                if i == j:
                    continue
                f.write(f"s.t. EVITAR_SUPERPOS_{i}{j}: {m_mayuscula} * YL{i}{j} + I{j} - F{i} >= 0;\n")
                f.write(f"s.t. EVITAR_SUPERPOS_{j}{i}: {m_mayuscula} * YL{j}{i} + I{i} - F{j} >= 0;\n")
                f.write(f"s.t. SUPERPOS{i}{j}: YL{i}{j} + YL{j}{i} = 1;\n")

        # defino tiempo final
        for i in range(1, 10):
            f.write(f"s.t. FIN_{i}: T_FINAL - F{i} >= 0;\n")

        # defino incomp entre prenda i y prenda j
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                if i == j:
                    continue
                if j in incompatibles[i]:
                    for k in range(1, 10):
                        f.write(f"s.t. INCOMP_{k}{i}{j}: YP{k}{i} + YP{k}{j} <= 1;\n")

        # cada prenda se lava una sola vez
        for j in range(1, n+1):
            f.write(f"s.t. LAV_UNICO_{j}: ")
            for i in range(1, 10):
                f.write(f"YP{i}{j} ")
                if i != 9:
                    f.write("+ ")
            f.write("= 1;\n")

        # defino el tiempo de cada lavado
        for i in range(1, 10):
            for j in range(1, n + 1):
                t_ind = tiempo_individual[j]
                f.write(f"s.t. TIEMPO_LAVADO_{i}{j}: T{i} - YP{i}{j} * {t_ind} >= 0;\n")

        # defino la solucion
        f.write("minimize z: T_FINAL;")
