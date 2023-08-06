import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# Cargamos el dataset en un DataFrame
films = pd.read_csv('Films.csv')

# Funciones para los endpoints solicitados

@app.get('/peliculas_idioma/')
def peliculas_idioma(Idioma: str):
    count_peliculas = films[films['original_language'] == Idioma].shape[0]
    return f"{count_peliculas} películas fueron estrenadas en idioma {Idioma}"

@app.get('/peliculas_duracion/{Pelicula}')
def peliculas_duracion(Pelicula: str):
    pelicula_data = films[films['title'] == Pelicula]
    
    if not pelicula_data.empty:
        duracion = pelicula_data.iloc[0]['runtime']
        ano_lanzamiento = pelicula_data.iloc[0]['release_date']
        return f"{Pelicula}. Duración: {duracion}. Año: {ano_lanzamiento}"
    else:
        return {"message": "La película no se encuentra en el dataset"}

@app.get('/franquicia/')
def franquicia(Franquicia: str):
    franquicia_data = films[films['belongs_to_collection'] == Franquicia]
    peliculas_count = franquicia_data.shape[0]
    ganancia_total = franquicia_data['revenue'].sum()
    ganancia_promedio = ganancia_total / peliculas_count
    return f"La franquicia {Franquicia} posee {peliculas_count} peliculas, una ganancia total de {ganancia_total} y una ganancia promedio de {ganancia_promedio}"

@app.get('/peliculas_pais/')
def peliculas_pais(Pais: str):
    count_peliculas = films[films['production_countries'] == Pais].shape[0]
    return f"Se produjeron {count_peliculas} películas en el país {Pais}"

@app.get('/productoras_exitosas/')
def productoras_exitosas(Productora: str):
    productora_data = films[films['production_companies'] == Productora]
    revenue_total = productora_data['revenue'].sum()
    peliculas_count = productora_data.shape[0]
    return f"La productora {Productora} ha tenido un revenue de {revenue_total} y ha realizado {peliculas_count} películas"

@app.get('/get_director/')
def get_director(nombre_director: str):
    resultado = []
    director_data = films[films['director'] == nombre_director]
    
    if not director_data.empty:
        total_return = director_data['return'].sum()  # Calculate total return
        for _, row in director_data.iterrows():
            pelicula_info = {
                "nombre_pelicula": row['title'],
                "fecha_lanzamiento": row['release_date'],
                "retorno_individual": row['return'],
                "costo": row['budget'],
                "ganancia": row['revenue']
            }
            resultado.append(pelicula_info)
        return {
            "director": nombre_director,
            "exito": total_return,
            "peliculas": resultado
        }
    else:
        return {"message": "El director no se encuentra en el dataset"}


# Eliminamos filas con valores faltantes en las columnas relevantes para el análisis
Films.dropna(subset=['belongs_to_collection', 'genres', 'release_date'], inplace=True)
Films['title'] = Films['title'].str.lower().str.strip()

Films['combined_features'] = (
    Films['belongs_to_collection'].astype(str) + ' ' +
    Films['genres'].astype(str) + ' ' +
    Films['release_date'].astype(str)
)

films = pd.read_csv('Films.csv')

# Crear la matriz de características TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(Films['combined_features'])

# Calcular la similitud del coseno utilizando el kernel lineal
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def recomendacion(titulo: str) -> List[str]:
    # Convertir el título ingresado a minúsculas y eliminar espacios en blanco
    titulo = titulo.lower().strip()

    # Realizar búsqueda difusa para encontrar el título más similar en el DataFrame
    match_scores = Films['title'].apply(lambda x: fuzz.partial_ratio(x.lower().strip(), titulo))
    best_match_index = match_scores.idxmax()

    # Obtener el índice de la película correspondiente al título más similar
    index = best_match_index

    # Calcular la similitud de la película con el resto de películas
    sim_scores = list(enumerate(cosine_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener los índices de las 5 películas más similares (excluyendo la película consultada)
    similar_movies_indices = [i[0] for i in sim_scores[1:6]]

    # Obtener los nombres de las películas recomendadas
    recommended_movies = Films['title'].iloc[similar_movies_indices].tolist()
    
    return recommended_movies

@app.get('/')
def get_recommendations(titulo: str):
    return recomendacion(titulo)




