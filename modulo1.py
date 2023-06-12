import requests
import random
import json
#coder-DReyes
API_KEY = 'your api code'


def guardar_detalles_peliculas(peliculas):
    datos_peliculas = []
    for i, pelicula in enumerate(peliculas, start=1):
        datos_pelicula = {
            'id_personalizado': i,
            'titulo': pelicula['title'],
            'generos': [genero['name'] for genero in pelicula['genres']],
            'director': obtener_director(pelicula),
            'actor_principal': obtener_actor_principal(pelicula),
            'palabras_clave': obtener_palabras_clave(pelicula['id'])
        }
        datos_peliculas.append(datos_pelicula)

    with open('detalles_peliculas.json', 'w') as file:
        json.dump(datos_peliculas, file, indent=4)

def obtener_director(pelicula):
    creditos_pelicula = obtener_creditos_pelicula(pelicula['id'])
    if creditos_pelicula:
        crew = creditos_pelicula['crew']
        directores = [miembro['name'] for miembro in crew if miembro['job'] == 'Director']
        if directores:
            return directores[0]
    return None

def obtener_actor_principal(pelicula):
    creditos_pelicula = obtener_creditos_pelicula(pelicula['id'])
    if creditos_pelicula:
        actores_principales = [actor['name'] for actor in creditos_pelicula['cast'][:1]]
        if actores_principales:
            return actores_principales[0]
    return None

# Obtén los detalles de una película específica
def obtener_detalles_pelicula(id_pelicula):
    url = f'https://api.themoviedb.org/3/movie/{id_pelicula}?api_key={API_KEY}'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos
    else:
        print(f'Error al obtener los detalles de la película con ID {id_pelicula}.')
        return None

# Obtén los créditos de una película específica
def obtener_creditos_pelicula(id_pelicula):
    url = f'https://api.themoviedb.org/3/movie/{id_pelicula}/credits?api_key={API_KEY}'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos
    else:
        print(f'Error al obtener los créditos de la película con ID {id_pelicula}.')
        return None

# Obtén las palabras clave de una película específica
def obtener_palabras_clave(id_pelicula):
    url = f'https://api.themoviedb.org/3/movie/{id_pelicula}/keywords?api_key={API_KEY}'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        palabras_clave = [palabra['name'] for palabra in datos['keywords']]
        return palabras_clave
    else:
        print(f'Error al obtener las palabras clave de la película con ID {id_pelicula}.')
        return None

# Obtén una lista de películas aleatorias
def obtener_peliculas_aleatorias(cantidad):
    peliculas = []
    peliculas_ids = set()  # Conjunto para almacenar los IDs de las películas ya seleccionadas
    while len(peliculas) < cantidad:
        id_pelicula = random.randint(1, 10000)
        if id_pelicula not in peliculas_ids:  # Verificar si el ID ya ha sido seleccionado
            detalles_pelicula = obtener_detalles_pelicula(id_pelicula)
            if detalles_pelicula:
                peliculas.append(detalles_pelicula)
                peliculas_ids.add(id_pelicula)  # Agregar el ID a la lista de IDs seleccionados
    return peliculas

# Obtener películas aleatorias y mostrar detalles
peliculas_aleatorias = obtener_peliculas_aleatorias(200)
guardar_detalles_peliculas(peliculas_aleatorias)
