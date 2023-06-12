import sys
import json
#coder-DReyes
def construir_grafo_ponderado(archivo_json):
    with open(archivo_json, 'r') as file:
        detalles_peliculas = json.load(file)

    grafo_ponderado = []
    peliculas_nombres = []
    enlaces_visitados = set()  # Conjunto para almacenar conexiones visitadas

    for i, pelicula in enumerate(detalles_peliculas, start=1):
        peliculas_nombres.append((i, pelicula['titulo']))
        for j, otra_pelicula in enumerate(detalles_peliculas, start=1):
            if i != j:
                ponderacion = 0

                if pelicula['director'] == otra_pelicula['director']:
                    ponderacion += 6

                for genero in pelicula['generos']:
                    if genero in otra_pelicula['generos']:
                        ponderacion += 3

                if pelicula['actor_principal'] == otra_pelicula['actor_principal']:
                    ponderacion += 5

                for palabra_clave in pelicula['palabras_clave']:
                    if palabra_clave in otra_pelicula['palabras_clave']:
                        ponderacion += 1

                if ponderacion > 0:
                    # Comprobar si la conexión ya existe en el grafo ponderado
                    enlace = (i, j, ponderacion)
                    enlace_inverso = (j, i, ponderacion)
                    if enlace not in enlaces_visitados and enlace_inverso not in enlaces_visitados:
                        grafo_ponderado.append(enlace)
                        enlaces_visitados.add(enlace)

    return grafo_ponderado, peliculas_nombres

def guardar_lista_en_archivo(lista, archivo):
    with open(archivo, 'w') as file:
        for item in lista:
            file.write(str(item) + '\n')

# Verificar si se proporcionó el nombre del archivo JSON como argumento
if len(sys.argv) > 1:
    archivo_json = sys.argv[1]
else:
    print("Debe proporcionar el nombre del archivo JSON como argumento al ejecutar el script.")
    sys.exit(1)

# Construir el grafo ponderado y obtener las listas de enlaces y nombres de películas
grafo_ponderado, peliculas_nombres = construir_grafo_ponderado(archivo_json)

# Guardar las listas en archivos de texto
guardar_lista_en_archivo(grafo_ponderado, 'enlaces_ponderados.txt')
guardar_lista_en_archivo(peliculas_nombres, 'nombres_peliculas.txt')
