def importar():
	n = 0
	incompatibles = {}
	tiempo_individual = {}

	f = open("problema1.py", "r")
	for linea in f:
		linea_split = linea.split()
		if linea_split[0] == "p":
			n = int(linea_split[2])
			e = int(linea_split[3])
			for i in range(1, n+1):
				incompatibles[i] = []
		elif linea_split[0] == "e":
			incompatibles[int(linea_split[1])].append(int(linea_split[2]))
		elif linea_split[0] == "n":
			tiempo_individual[int(linea_split[1])] = int(linea_split[2])
	return incompatibles, tiempo_individual, n

def es_compatible(prenda, prendas_a_comparar, incompatibles):
	#Determina si una prenda es compatible con una lista de prendas
	for p in prendas_a_comparar:
		if p in incompatibles[prenda]:
			return False
	return True

def compatibles(prenda, incompatibles, n):
	#Obtiene todas las prendas compatibles con una
	compatibles = []
	for p in range(1, n+1):
		if (p != prenda) and (p not in incompatibles[prenda]):
			compatibles.append(p)
	return compatibles


# Algoritmo
def obtener_combinaciones():
	#agrupando en orden de prenda
	incompatibles, tiempo_individual, n = importar()
	prendas_no_lavadas = []
	combinaciones = []

	#guardo las prendas que aun no fueron guardadas
	for p in range(1, n+1):
		prendas_no_lavadas.append(p)

	while len(prendas_no_lavadas) != 0:
		#tomo una prenda que aun no fue lavada
		prox_a_lavar = prendas_no_lavadas[0]
		prendas_no_lavadas.remove(prox_a_lavar)

		prendas_a_lavar = [prox_a_lavar]

		#tomo las prendas que no fueron lavadas y son compatibles con las que estan en el lavarropas
		for i in compatibles(prox_a_lavar, incompatibles, n):
			if i not in prendas_no_lavadas:
				continue
			if es_compatible(i, prendas_a_lavar, incompatibles):
				prendas_a_lavar.append(i)
				prendas_no_lavadas.remove(i)

		#cuando no hay mas prendas compatibles se inicia el lavarropas
		combinaciones.append(prendas_a_lavar)

	return combinaciones

print(obtener_combinaciones())
