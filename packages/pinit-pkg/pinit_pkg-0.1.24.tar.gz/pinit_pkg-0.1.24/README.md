# clusters-ml-service
Este repositorio contiene notebooks y scripts relacionados con el servicio de clustering utilizando Machine Learning.

## Insumos para este servicio
A continuación, se describe la estructura de los archivos de entrada requeridos para procesar y clusterizar ubicaciones geográficas. El sistema recibe dos tipos de archivos:
* Un archivo JSON con los parámetros de configuración.
* Un archivo CSV o Parquet con las coordenadas geográficas de los puntos a clusterizar.

### 1. Formato del archivo JSON de configuración
El archivo JSON contiene los parámetros que controlan la ejecución del proceso de clustering. Se debe nombrar siguiendo el formato:
```
params_YYYY_MM_DD.json
```
donde:

* `YYYY` es el año.
* `MM` es el mes.
* `DD` es el día.

#### Descripción de los parámetros:

| Parámetro                        | Tipo    | Descripción |
|----------------------------------|--------|-------------|
| `file_name`                    | `str`  | Ruta de la carpeta donde están los archivos de puntos. |
| `remove_outliers`                | `bool` | Indica si se deben eliminar outliers (`true` o `false`). |
| `outlier_filter_level`           | `str`  | Nivel de sensibilidad en la detección de outliers: `"estricto"`, `"moderado"`, `"relajado"`. <br> <br> Este parámetro permite ajustar qué tan estrictamente se eliminan los puntos que podrían ser errores o ubicaciones poco comunes. Se pueden usar tres niveles: <br> * **"estricto"** → Filtra puntos más alejados, incluso si aún están en la zona de cobertura. <br> * **"moderado"** (recomendado) → Permite más variabilidad, eliminando solo puntos extremos. <br> * **"relajado"** → Solo filtra puntos extremadamente lejanos. <br> <br> Si no estás seguro de qué nivel usar, prueba primero `"moderado"`.|
| `max_cluster_percentage`                         | `int`  | Límite máximo de % de paquetes en un mismo cluster (0 a 100, default: `40`). |
| `min_packages_per_cluster_enabled` | `bool` | Indica si se debe aplicar una restricción sobre el número mínimo de paquetes por cluster (`true` o `false`).  |
| `min_packages_per_cluster`       | `int`  | Valor mínimo de paquetes por cluster, requerido si `min_packages_per_cluster_enabled` es `true`. |


#### Ejemplo:

```json
{
  "file_name": "data_2025_03_03.parquet",
  "remove_outliers": true,
  "outlier_filter_level": "moderado",
  "max_cluster_percentage": 40,
  "min_packages_per_cluster_enabled": true,
  "min_packages_per_cluster": 5
}
```


### 2. Formato del archivo de coordenadas (CSV o Parquet)

El archivo que contiene las coordenadas debe ser en formato CSV o Parquet y debe llamarse:
```
data_YYYY_MM_DD.csv  
data_YYYY_MM_DD.parquet
```
dependiendo del formato elegido.

#### Estructura del archivo

El archivo debe contener dos columnas obligatorias:

| Columna    | Tipo    | Rango válido  | Descripción |
|------------|--------|---------------|-------------|
| `id`  | `int` o `str` | No aplica| Identificador del punto (este campo es opcional). |
| `latitude`  | `Float` | -90 a 90      | Latitud geográfica del punto. |
| `longitude` | `Float` | -180 a 180    | Longitud geográfica del punto. |

Si el archivo contiene nulo en alguna coordenada se eliminará ese registro del proceso.

#### Ejemplo:

```csv
id,latitude,longitude
1,19.4326,-99.1332
2,34.0522,-118.2437
3,40.7128,-74.0060
```

## Salidas de este servicio

El servicio genera tres archivos de salida, proporcionando información sobre los clusters detectados y facilitando su visualización.  

### 1. Archivo de Clusters y Centroides (`clusters_yyyy_mm_dd.csv`)  
Contiene los centroides de cada cluster.

| Columna        | Tipo   | Descripción |
|---------------|--------|-------------|
| `cluster`     | `int`  | Identificador del cluster. <br> Nota: Si el punto es identificado como outlier, el cluster será -1. |
| `latitude`    | `float` | Latitud del centroide del cluster. |
| `longitude`   | `float` | Longitud del centroide del cluster. |

#### Ejemplo

```csv
cluster,latitude,longitude
1,19.4326,-99.1332
2,40.7128,-74.0060
```

### 2. Archivo de Puntos con Clusters (`puntos_yyyy_mm_dd.csv`)  

Incluye cada punto de entrada con su cluster asignado.  

| Columna     | Tipo   | Descripción |
|------------|--------|-------------|
| `id`       | `int`  | Identificador único del punto (si venía en el archivo de entrada). |
| `latitude` | `float` | Latitud del punto. |
| `longitude`| `float` | Longitud del punto. |
| `cluster`  | `int`  | Cluster asignado al punto. |

#### Ejemplo

```csv
id,latitude,longitude,cluster 
1,19.4326,-99.1332,1 
2,40.7128,-74.0060,2
```


### 3. Archivo para Google Earth (`puntos_yyyy_mm_dd.kmz`)  

Archivo en formato `.kmz` que permite visualizar los clusters en **Google Earth**.  

- Los puntos individuales se muestra con un **marcador** en sus coordenadas coloreados según su cluster.  
- Permite explorar de manera interactiva la distribución de los clusters.  

Para visualizarlo: 
1. Descargar el archivo `.kmz`.  
2. Abrirlo en **Google Earth** o cualquier software compatible con este formato.  
3. Explorar la distribución geográfica de los clusters.  

### 4. Mensaje sobre el proceso ejecutado

Mensaje de salida que confirma la cantidad de datos procesados, clusters creados, tiempo de ejecución, archivos generados.

#### Ejemplo

```txt
Proceso de clustering completado con éxito.

Resumen del proceso:
  - Total de puntos en el archivo: 263
  - Total de puntos procesados: 262
  - Total de clusters generados: 9
  - Puntos considerados outliers y excluidos: 2
  - Tiempo total de ejecución: 4.60 segundos

Archivos generados:
  - Clusters y centroides: clusters_2025_03_05.csv
  - Puntos con clusters asignados: puntos_2025_03_05.csv
  - Archivo KMZ para Google Earth: clusters_2025_03_05.kmz






