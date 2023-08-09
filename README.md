PROYECTO INDIVIDUAL Nº1: Machine Learning Operations (MLOps)



![image](https://github.com/FedeGG09/PROYECTO-INDIVIDUAL-NUMERO1/assets/124220922/922814e2-eecf-474f-9015-79312b21a978)



![image](https://github.com/FedeGG09/PROYECTO-INDIVIDUAL-NUMERO1/assets/124220922/92ba208b-4aa8-4593-8599-7398859dba6c)

Link al Deploy en RENDER: https://fedegravinahenryp1.onrender.com/docs
Link al video presentación: https://clipchamp.com/watch/fEE2Dqeagwj


Este es el primer proyecto individual de la etapa de Labs en el Bootcamp de Henry. Este trabajo  nos sitúa en el rol de un MLOps Engineer

Se nos proporciono dos datasets en formato csv (coma separated values) con información de películas que constaba de diferentes campos, como el año de estreno, actores, directores, presupuesto, entre otros.

                                                                      ETL

La primera tarea constó en realizar un proceso de ETL (Extract, Transform and Load) en donde llevé a cabo una limpieza de los datos crudos en la plataforma Visual Studio Code con lenguaje Python.
Como primer paso, cargué y combiné ambos Dataset en un DataFrame de Pandas para tener todos los datos a disposición.
Dado que los datos proporcionados en algunos campos tenian un formato de diccionario o lista con información que no me servian para la realización del proyecto, continué el trabajo creando una función personalizada que los desanide y extraiga el contenido que era de mi interes. 
Un ejemplo de esta función es la aplicada a la columna belongs_to_collection:
 
def extract_collection_name(collection):
    try:
        return ast.literal_eval(collection)['name']
    except (ValueError, TypeError):
        return None

Films['belongs_to_collection'] = Films['belongs_to_collection'].apply(extract_collection_name)

Con este código conseguí desarmar el diccionario que indicaba a que serie de películas pertenecen y quedarme unicamente con el nombre de la franquicia.
Luego apliqué funciones similares para completar el proceso de limpieza de datos y quedarme solo con lo que me interesaba para poder seguir con los pasos siguientes.

Una vez terminado el paso anterior, el proceso continuó llenando los datos invalidos con datos que me permitieran luego utilizar esas columnas para realziar comparaciones y los procesos de EDA y luego crear mi sistema de recomendación.

Ejemplos de estos códigos son:


Films['budget'].fillna(0, inplace=True)


Films.dropna(subset=['release_date'], inplace=True)

El siguiente paso fue cambiar las fechas de estreno para hacerlas coincidir con el formato pedido en la consigna: AAAA:MM:DD

Films['release_date'] = pd.to_datetime(Films['release_date'], errors='coerce')

Films.dropna(subset=['release_date'], inplace=True)

Films['release_date'] = Films['release_date'].dt.strftime('%Y-%m-%d')

Luego creé una nueva columna en el DataFrame llamada return que calcula el retorno de inversión de cada película.

def calculate_return(row):
    revenue = pd.to_numeric(row['revenue'], errors='coerce')
    budget = pd.to_numeric(row['budget'], errors='coerce')
    if pd.notna(revenue) and pd.notna(budget) and budget != 0:
        return revenue / budget
    return 0

Films['return'] = Films.apply(calculate_return, axis=1)

Una vez concluido este paso eliminé las columnas que no necesitaba y tuve que realizar un corte en las filas de las películas, basado en las fechas de estreno, dado que no me interesaba para el modelo tener películas anteriores a 1960. El objetivo real de este paso era achicar el archivo csv para que tenga un tamaño que me permitiera subirlo a un repositorio de Github y luego hacer un deploy en la página Render.com

Films['release_date'] = pd.to_datetime(Films['release_date'])

fecha_inicio = pd.to_datetime('1960-12-01')
fecha_fin = pd.to_datetime('2022-12-01')

Films = Films[(Films['release_date'] >= fecha_inicio) & (Films['release_date'] <= fecha_fin)]


EDA


El siguiente paso para el proyecto consistió en realizar el EDA (Análisis exploratorio de datos).
Durante este proceso, realicé estadísticas descriptivas de los campos, distribución de las variables numéricas, matriz de relaciones sobre el DataFrame “Films” que fue el que resultó de todo el proceso anterior. 
Ejemplos de código: 

correlation_matrix = Films.corr()

print(Films.describe())

Realicé gráficos de estas relaciones y obtuve indicios de que me interesaba concatenar luego para los pasos siguientes del proyecto. Debido a las consignas del proyecto, no fue necesario realiza un análisis a fondo, pero en otro tipo de trabajos, sería en este momento en donde me dedicaría a hacer una exploración a fondo de las variables, a realizar gráficos y verificar relaciones para sacar conclusiones y poder, a partir de estas, hacer un análsis de los datos y realizar un informe o seguir adelante y llevar a cabo un proceso de Machine Learning. Un ejemplo de estos es el siguiente:

![image](https://github.com/FedeGG09/PROYECTO-INDIVIDUAL-NUMERO1/assets/124220922/12bfe42e-e3d0-439c-afba-d8caf9f682ce)


DESARROLLO DE LAS CONSULTAS A LA API:

Desarrollado en Visual Studio Code y siguiendo las consignas otorgadas, procedí a desarrollar 6 funciones en Python para luego poder ser desplegadas en un repositorio nuevo de mi GitHub desde FastApi. Un ejemplo de estas consultas consistio en realizar función que se utiliza para consultar información sobre una franquicia de películas específica, incluido el número de películas, la ganancia total y la ganancia promedio de las películas en esa franquicia. 

@app.get('/franquicia/')
def franquicia(Franquicia: str):
    franquicia_data = films[films['belongs_to_collection'] == Franquicia]
    peliculas_count = franquicia_data.shape[0]
    ganancia_total = franquicia_data['revenue'].sum()
    ganancia_promedio = ganancia_total / peliculas_count
    return f"La franquicia {Franquicia} posee {peliculas_count} peliculas, una ganancia total de {ganancia_total} y una ganancia promedio de {ganancia_promedio}"

En este ejemplo defino la fución franquicia como cadena de caracteres y creo las variables franquicia_data(en donde cargo los datos pertinentes desde mi dataset ya limpio “films”)
A continuación defino la variable “peliculas_count “ donde calculo el
número de películas en la franquicia seleccionada contando la cantidad de filas en el DataFrame de la variable anterior.
Creo una nueva variable llamada “ganancia_total” donde calculo la ganancia total de la franquicia seleccionada sumando los valores de la columna 'revenue' en el DataFrame "franquicia_data". 
Finalmente utilizo “ganancia_promedio” dividiendo la ganancia total entre el número de películas en la franquicia.
En la última línea de código le pido a la función que me devuelva una cadena formateada que contenga el: nombre de la franquicia, cantidad de películas, ganancia total y ganancia promedio.


DESARROLLO DE LAS CONSULTAS A LA API

Desarrollado en Visual Studio Code y siguiendo las consignas otorgadas, procedí a desarrollar 6 funciones en Python para luego poder ser desplegadas en un repositorio nuevo de mi GitHub desde FastApi. Un ejemplo de estas consultas consistio en realizar función que se utiliza para consultar información sobre una franquicia de películas específica, incluido el número de películas, la ganancia total y la ganancia promedio de las películas en esa franquicia. 

@app.get('/franquicia/')
def franquicia(Franquicia: str):
    franquicia_data = films[films['belongs_to_collection'] == Franquicia]
    peliculas_count = franquicia_data.shape[0]
    ganancia_total = franquicia_data['revenue'].sum()
    ganancia_promedio = ganancia_total / peliculas_count
    return f"La franquicia {Franquicia} posee {peliculas_count} peliculas, una ganancia total de {ganancia_total} y una ganancia promedio de {ganancia_promedio}"

En este ejemplo defino la fución franquicia como cadena de caracteres y creo las variables franquicia_data(en donde cargo los datos pertinentes desde mi Dataset ya limpio “films”)
A continuación defino la variable “peliculas_count “ donde calculo el
número de películas en la franquicia seleccionada contando la cantidad de filas en el DataFrame de la variable anterior.
Creo una nueva variable llamada “ganancia_total” donde calculo la ganancia total de la franquicia seleccionada sumando los valores de la columna 'revenue' en el DataFrame "franquicia_data". 
Finalmente utilizo “ganancia_promedio” dividiendo la ganancia total entre el número de películas en la franquicia.
En la última línea de código le pido a la función que me devuelva una cadena formateada que contenga el: nombre de la franquicia, cantidad de películas, ganancia total y ganancia promedio.


SISTEMA DE RECOMENDACIÓN DE PELÍCULAS

La parte final del proyecto consistió en realizar un proceso de Machine Learning para seleccionar una película y que me devuelva cinco películas similares.
Con este objeto, empecé por importar las librerías que voy a utilizar de Pandas y  Scikit-learn. Cargué el DataFrame ya limpio, estandarice las columnas que me interesaban para entrecruzar y recomendar. 
Utilice estos campos:

Films['combined_features'] = (
    Films['belongs_to_collection'].astype(str) + ' ' +
    Films['genres'].astype(str) + ' ' +
    Films['release_date'].astype(str) + ' ' +
    Films['original_language'].astype(str)
)

A continuación cree una matriz de características TF-IDF. Aquí lo utilizo para calcular la similitud del coseno entre documentos de texto que han sido representados numéricamente mediante esta técnica. El resultado es una matriz de similitud del coseno que puede ser utilizada para encontrar documentos similares en función de sus características.
Finalmente llamo a la librería fuzzywuzzy para conseguir que cuando el usuario escriba el titulo de una película, el programa acepte errores de tipeo.
Finalmente creo la función “recomendación”. 
Aquí utilizo el código que explico a continuación para desarrollar mi Sistema de Recomendación de Películas.

1.	titulo = titulo.lower().strip(): Convierte el título ingresado a minúsculas y elimina los espacios en blanco al principio y al final.

2.	match_scores = Films['title'].apply(lambda x: fuzz.partial_ratio(x.lower().strip(), titulo)): Utiliza la función fuzz.partial_ratio de la librería FuzzyWuzzy para calcular puntuaciones de similitud difusa entre el título ingresado y todos los títulos en la columna 'title' del DataFrame Films. Esta línea crea una serie de puntuaciones de similitud.


3.	best_match_index = match_scores.idxmax(): Encuentra el índice de la película con la puntuación de similitud más alta en la serie de puntuaciones de similitud calculadas anteriormente.

4.	index = best_match_index: Almacena el índice de la película más similar en la variable index.


5.	sim_scores = list(enumerate(cosine_sim[index])): Obtiene la lista de puntuaciones de similitud del coseno entre la película seleccionada y todas las demás películas en la matriz de similitud cosine_sim.

6.	sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True): Ordena las puntuaciones de similitud en orden descendente para obtener las películas más similares en primer lugar.


7.	similar_movies_indices = [i[0] for i in sim_scores[1:6]]: Obtiene los índices de las 5 películas más similares (excluyendo la película consultada) de la lista ordenada de puntuaciones de similitud.
8.	recommended_movies = Films['title'].iloc[similar_movies_indices].to_list(): Obtiene los nombres de las películas recomendadas utilizando los índices de las películas más similares y los busca en la columna 'title' del DataFrame Films. Los nombres se almacenan en la lista recommended_movies.

9.	return recommended_movies: Devuelve la lista de nombres de películas recomendadas.


Para terminar el proyecto subo las librerias que consumiran la api en el archivo requirements.txt y el código en el archivo main.py.
El paso final consistió en desplegar el proyecto en la página Render.com a través de la clonación de este repositorio en dicha página.

Muchas Gracias por la atención.
