# Proyecto entidades en recetas médicas
Repositorio para proyecto de reconocimiento de entidades en texto de recetas médicas en el contexo del ramo MDS7201 Proyecto de Ciencia de Datos, Universidad de Chile.

**Integrantes**:
- Daniel Carmona G. (Ing. Civil Eléctrica)
- Martín Sepúlveda (Ing. Civil Eléctrica)
- Monserrat Prado (Ing. Civil en Ciencias de la Computación)
- Camilo Carvajal Reyes (Ing. Civil Matemática)

**Colaboradores**:
- Patricio Wolff (Minsal)
- Constanza Contreras (Docente MDS7201)
- Francisco Förster (Docente MDS7201)

### Demo
Ponemos a disposición dos demostraciones de funcionamiento de nuestro trabajo (se restringe a los modelos BETO, pero un funcionamiento con RNN sería análogo).

1. [Demo general](demo_minsal/demo.ipynb)

    Este demo está listo para funcionar desde cero en cualquier máquina que tenga instalada python y jupyter notebooks. Instala las dependencias relevantes, descarga los modelos. Ejecuta las predicciones y las traduce a lenguaje entendible. El notebook puede ser usado de manera independiente de este repositorio.

2. [Demo minimalista](demo_minsal/demo_minimalista.ipynb)

    Este demo carga y usa los modelos para un texto de manera directa, sin que el usuario vea el código detrás. Es una manera de mostrar como funcionaría el modelo en producción y depende de el los scripts [predicciones](demo_minsal/predicciones.py) y [auxfunctions](modelos/auxfunctions.py). Este demo requiere un ambiente python donde se hayan instalado las dependencias usando

    ```pip install -r requirements.txt```


## Contenidos
Datos y códigos relevantes presentes en el repositorio.

### Datos
Los datos originales no se encuentran en este repositorio. Corresponden a datos de prescripciones de un hospital de la región metropolitana.

**Exploraciones**
- [Primer EDA](datos/MINSAL_ENTIDADES_MDS7201.ipynb)
- [Análisis principio activo](exploracion/EDA_PrincipioActivo.ipynb)
- [Exploracion columnas complementarias](exploracion/exploracion_complementaria.ipynb)

### Modelos
- **[LSTM (baseline)](modelos/Baseline/Baseline.ipynb)**
- **Expresiones regulares** - [Primera versión](datos/Etiquetado/Expresiones_Regulares_Minsal.ipynb) - [Segunda versión](datos/Etiquetado/RegExV2.0.ipynb)
- **BETO clinico** - [modelo general](modelos/token_clf_HF.ipynb) - [modelo ADMIN](modelos/token_clf_admins_HF.ipynb)

Los modelos BETO están disponibles en el repositorio HuggingFace transformers:
- [beto-prescripciones-medicas](https://huggingface.co/ccarvajal/beto-prescripciones-medicas) 
- [beto-prescripciones-medicas-ADMIN](https://huggingface.co/ccarvajal/beto-prescripciones-medicas-ADMIN)

## Resumen de resultados
A continuación se reportan las métricas de los modelos desarrollados en este repositorio
| modelo | f1 | precision | recall |
|---|:---:|---|---|
| RegEx | 0.56 | 0.94 | 0.48 |
| RNN | 0.68 | 0.74 | 0.64 |
| RNN fine-tunning | 0.92 | 0.92 | 0.92 |
| BETO | 0.83 | 0.86 | 0.90 |
| BETO fine-tunning | 0.93 | 0.92 | 0.94 |
| RNN ADMIN | 0.93 | 0.93 | 0.94 |
| BETO ADMIN | 0.94 | 0.93 | 0.95 |


## Presentaciones
- [1. Comprensión y objetivos](presentaciones/Presentación_1_MDS7201_Comprensión_y_objetivos.pdf)
- [2. Análisis exploratorio de datos](presentaciones/Presentación_2_MDS7201_Análisis_exploratorio.pdf)
- [3. Definición de proyecto](presentaciones/Presentación_3_MDS7201_Proyecto_definido.pdf)
- [4. Solución al problema](presentaciones/Presentación_4_MDS7201_Solucion_al_problema.pdf)
- [5. Presentación Final](presentaciones/Presentación_5_MDS7201_Presentacion_final.pdf)
- [6. Presentación Workshop Minsal](presentaciones/Presentación_Minsal_MDS7201_Workshop.pdf)
