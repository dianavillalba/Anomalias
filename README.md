# Anomalias
MIAD Proyecto aplicado en analítica de datos


## Tabla de Contenido

- [Introducción](#Introducción)
    - [Pregunta de negocio](#Pregunta-de-negocio)
    - [Motivación](#Motivación)
- [Repositorio](#Repositorio)
    - [Niveles](#Niveles)
    - [Ejecución](#Ejecución)
- [Características](#Características)
- [¿Como funciona?](#¿Como-funciona?)
    - [Diagrama de proceso](#Diagrama-de-proceso)
- [Requerimientos](#Requerimientos)
- [Artículos](#Artículos)

## Introducción
### Pregunta de negocio

<br>
<br>
### Motivación
???

<p align="center">
  <img src="./img/img2.png" alt="Size Limit CLI" width="738">
</p>

## Repositorio
### Niveles
Contamos con 3 carpetas principales
- data (Insumos principales .csv)
- img (Imagenes relacionadas en el documento)
- scripts (Codigo .ipynb)

### Ejecución
Puedes ejecutar el codigo desde sitios como (Google Colab, Jupiter Notebook o VSC)
una vez escojas el ambiente donde vas a desplegar asegurate de usar una version de python superior a la 3.5

para verificar la version puedes ejecutar el siguiente comando:

```bash
!python --version
```

una vez tengas la versión nesesaria installa las siguientes dependencias como sigue

```bash
!pip install -r requirements.txt
```
Apartir de acá ya puedes ejecutar el notebook y probar la aplicación

## Características del tablero de control

El tablero de control tiene como objetivo el análisis y detección de anomalías en el comportamiento del consumo de energía de los clientes no regulados propios y terceros de ElectroDunas. Esta herramienta facilita la visualización del consumo histórico, la detección de anomalías y la predicción de comportamientos futuros, permitiendo una gestión más eficiente y proactiva del suministro eléctrico.

### Datos utilizados:
*	Periodo disponible: Desde el 1 de enero de 2021 hasta el 1 de abril de 2023.
*	Variables: Energía activa (kWh), energía reactiva (kVarh), Sector económico e ID cliente.
*	Cantidad de clientes: 15 clientes analizados con alta completitud de datos (≥ 99%).

### Metodología – Modelos
*	Detección de anomalías: implementación de modelos no supervisados y series de tiempo tales como DBSCAN y KernelCPD.
*	Predicción consumo: SVR (Support Vector Regression) y LSTM (Long Short-Term Memory)
*	Clasificación anomalías futuras: Random Forest y Gradient Boosting

### Interactividad y Funcionalidades
*	Filtros Dinámicos: Permiten explorar y segmentar los datos según diferentes criterios tales como el sector económico, intervalo de tiempo (fecha inicio y fecha fin), ID cliente, nivel de confianza del pronóstico y periodo de pronostico
*	Alertas de Anomalías: Notificaciones visuales cuando se detectan patrones de consumo atípicos tanto a nivel histórico como patrones futuros.
*	Cuadro resumen con la información de las anomalías detectadas según el periodo seleccionado con la información del registro exacto y su desviación.

## Requerimientos Técnicos
* Linux or macOS or Windows
* bash
* * version > python 3.5
* Frontend: Dash y Bootstrap
* Modelos Analíticos: Scikit-learn, TensorFlow

## Referencias
Banik, S., Saha, S. K., Banik, T., & Hossain, S. M. M. (2023). Anomaly Detection Techniques in Smart Grid Systems: A Review (arXiv:2306.02473). arXiv. http://arxiv.org/abs/2306.02473 

Chiosa, R., Piscitelli, M. S., Fan, C., & Capozzoli, A. (2022). Towards a self-tuned data analytics-based process for an automatic context-aware detection and diagnosis of anomalies in building energy consumption timeseries. Energy and Buildings, 270, 112302. https://doi.org/10.1016/j.enbuild.2022.112302 

Farag, A., Abdelkader, H., & Salem, R. (2022). Parallel graph-based anomaly detection technique for sequential data. Journal of King Saud University - Computer and Information Sciences, 34(1), 1446-1454. https://doi.org/10.1016/j.jksuci.2019.09.009 

Feasel, K. (2022). Finding Ghosts in Your Data: Anomaly Detection Techniques with Examples in Python; Apress: Berkeley, CA, USA, 2022;

Maleki, S., Maleki, S., & Jennings, N. R. (2021). Unsupervised anomaly detection with LSTM autoencoders using statistical data-filtering. Applied Soft Computing, 108, 107443. https://doi.org/10.1016/j.asoc.2021.107443 

Monedero, I., Biscarri, F., León, C., Guerrero, J. I., Biscarri, J., & Millán, R. (2012). Detection of frauds and other non-technical losses in a power utility using Pearson coefficient, Bayesian networks and decision trees. International Journal of Electrical Power & Energy Systems, 34(1), 90-98. https://doi.org/10.1016/j.ijepes.2011.09.009 

Schneider, P., & Xhafa, F. (2022). Anomaly detection. En Anomaly Detection and Complex Event Processing over IoT Data Streams (pp. 49-66). Elsevier. https://doi.org/10.1016/B978-0-12- 823818-9.00013-4 

Wang, X., Yao, Z., & Papaefthymiou, M. (2023). A real-time electrical load forecasting and unsupervised anomaly detection framework. Applied Energy, 330, 120279. https://doi.org/10.1016/j.apenergy.2022.120279 

Xu, C., & Chen, H. (2020). A hybrid data mining approach for anomaly detection and evaluation in residential buildings energy data. Energy and Buildings, 215, 109864. https://doi.org/10.1016/j.enbuild.2020.109864 
