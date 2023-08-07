import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import fuzz
from typing import List
from fastapi import FastAPI

app = FastAPI()

# Cargamos el dataset en un DataFrame
films = pd.read_csv('Films.csv')

# Funciones para los endpoints solicitados

@app.get('/peliculas_idioma/')
def peliculas_idioma(Idioma: str):
    count_peliculas = films[films['original_language'] == Idioma].shape[0]
    return f"{count_peliculas} películas fueron estrenadas en idioma {Idioma}"

@app.get('/peliculas_duracion')
def peliculas_duracion(Pelicula: str):
    movie_data = films[films['title'] == Pelicula].iloc[0]
    return f"{Pelicula}. Duración: {movie_data['runtime']}. Año: {movie_data['release_date'][-4:]}"

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


films.dropna(subset=['belongs_to_collection', 'genres', 'release_date'], inplace=True)
films['title'] = films['title'].str.lower().str.strip()


films['combined_features'] = (
    films['belongs_to_collection'].astype(str) + ' ' +
    films['genres'].astype(str) + ' ' +
    films['release_date'].astype(str)
)


tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(films['combined_features'])


cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def get_recommendations(title: str) -> List[str]:
   
    title = title.lower().strip()

  
    match_scores = films['title'].apply(lambda x: fuzz.partial_ratio(x.lower().strip(), title))
    best_match_index = match_scores.idxmax()

  
    index = best_match_index


    sim_scores = list(enumerate(cosine_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

   
    top_indices = [i[0] for i in sim_scores[1:6]]


    recommended_movies = films['title'].iloc[top_indices].tolist()

    return recommended_movies


@app.get('/recommendation/{title}')
def recommend(title: str):
    recommendations = get_recommendations(title)
    return {'recommended_movies': recommendations}

    top_indices = [i[0] for i in similarity_scores[1:6]]
    top_movies = movies.iloc[top_indices]
    recommendations = top_movies['title'].tolist()

    return recommendations


