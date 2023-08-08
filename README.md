PROYECTO INDIVIDUAL Nº1: Machine Learning Operations (MLOps)



![image](https://github.com/FedeGG09/PROYECTO-INDIVIDUAL-NUMERO1/assets/124220922/922814e2-eecf-474f-9015-79312b21a978)



![image](https://github.com/FedeGG09/PROYECTO-INDIVIDUAL-NUMERO1/assets/124220922/92ba208b-4aa8-4593-8599-7398859dba6c)

Link al Deploy en RENDER: https://fedegravinahenryp1.onrender.com/docs

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





