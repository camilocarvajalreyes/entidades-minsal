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


## Contenidos

### Datos
Los datos originales no se encuentran en este repositorio. Corresponden a datos de prescripciones de un hospital de la región metropolitana.

**Exploraciones**
- [Primer EDA](datos/MINSAL_ENTIDADES_MDS7201.ipynb)
- [Análisis principio activo](exploracion/EDA_PrincipioActivo.ipynb)
- [Exploracion columnas complementarias](exploracion/exploracion_complementaria.ipynb)

### Modelos
- **[LSTM (baseline)](modelos/Baseline/Baseline.ipynb)**
- **Expresiones regulares** - [Primera versión](datos/Etiquetado/Expresiones_Regulares_Minsal.ipynb) - [Segunda versión](datos/Etiquetado/RegExV2.0.ipynb)
- **BERT clinico** - [entrenamiento](modelos/token_clf_HF.ipynb) - [evaluación](modelos/evaluacion_modelos.ipynb)


### Presentaciones
- [1. Comprensión y objetivos](presentaciones/Presentación_1_MDS7201_Comprensión_y_objetivos.pdf)
- [2. Análisis exploratorio de datos](presentaciones/Presentación_2_MDS7201_Análisis_exploratorio.pdf)
- [3. Definición de proyecto](presentaciones/Presentación_3_MDS7201_Proyecto_definido.pdf)
- [4. Solución al problema](presentaciones/Presentación_4_MDS7201_Solucion_al_problema.pdf)
- [6. Presentación Final]()
- [5. Presentación Workshop Minsal](presentaciones/Presentación_Minsal_MDS7201_Workshop.pdf)
