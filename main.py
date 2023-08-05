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

@app.get('/peliculas_duracion/')
def peliculas_duracion(Pelicula: str):
    pelicula_data = films[films['title'] == Pelicula]
    
    if not pelicula_data.empty:
        duracion = pelicula_data.iloc[0]['runtime']
        ano_lanzamiento = pelicula_data.iloc[0]['release_year']
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


@app.get('/recomendacion/')
def get_recomendacion(titulo: str):
    # Convert the input title to lowercase and remove whitespace
    titulo = titulo.lower().strip()

    # Perform fuzzy search to find the most similar title in the DataFrame
    match_scores = films['nombre_pelicula'].apply(lambda x: fuzz.partial_ratio(x.lower().strip(), titulo))
    best_match_index = match_scores.idxmax()

    # Calculate the similarity of the movie with the rest of the movies
    sim_scores = list(enumerate(cosine_sim[best_match_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top 5 similar movies (excluding the queried movie)
    similar_movies_indices = [i[0] for i in sim_scores[1:6]]

    # Get the names of the recommended movies
    recommended_movies = films['nombre_pelicula'].iloc[similar_movies_indices].to_list()

    return {"recommended_movies": recommended_movies}




