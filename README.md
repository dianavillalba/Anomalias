<table style="border-collapse: collapse; margin: 0 auto;">
  <tr style="border: none;">
    <td colspan="3" style="border: none; text-align: center;"><h3>          Proyecto aplicado en analítica de datos</h3></td>
  </tr>
  <tr style="border: none;">
    <td style="border: none;"><img src="static/img/miad.png" alt="Miad Logo" width="100"/></td>
    <td style="border: none;"><h1 align="center">Sistema de Detección de Anomalías </h1></td>
    <td style="border: none;"><img src="static/img/electrodunas.png" alt="Electro Dunas Logo" width="100"/></td>
  </tr>
</table>

## Tabla de Contenido

- [Introducción](#introducción)
  - [Contexto](#contexto)
  - [Planteamiento del problema de Negocio](#planteamiento-del-problema-de-negocio)
  
- [Características](#características)
  - [Datos utilizados](#datos-utilizados)
  - [Metodología – Modelos](#metodología--modelos)
  - [Interactividad y Funcionalidad](#interactividad-y-funcionalidad)
  
- [Repositorio](#repositorio)
  - [Niveles](#niveles)
  - [Ejecución](#ejecución)
  
- [Requerimientos Técnicos](#requerimientos-técnicos)
  
- [Referencias](#referencias)

## Introducción

### Contexto  

Electro Dunas, empresa peruana especializada en distribución de energía eléctrica, opera en las provincias de Ica, Huancavelica y Ayacucho, abarcando 5,402 km2 y atendiendo a 264,480. Desde su integración al Grupo Energía Bogotá en agosto de 2019, pertenece a un conglomerado líder en energía y gas natural en Colombia, Perú y Brasil. El GEB, comprometido con generar valor, bienestar comunitario y sostenibilidad ambiental, refleja la visión y enfoque de Electro Dunas. 
La empresa se desenvuelve en dos segmentos de mercado: el regulado y el de competencia. Este último se compone de clientes libres, tanto propios como terceros. A los clientes libres propios se les facturan los precios de generación según sus acuerdos contractuales, además de los cargos regulados por transmisión. Por otro lado, los clientes terceros son facturados de acuerdo con los cargos regulados por transmisión y/o distribución, en función de la utilización que hagan del sistema eléctrico de Electro Dunas. 

### Planteamiento del problema de Negocio 
Con un crecimiento significativo de clientes no regulados, la empresa se propone utilizar analítica de datos para identificar posibles anomalías en el comportamiento de sus clientes no regulados. El proyecto se enfoca en desarrollar un Producto Mínimo Viable (PMV) que visualice datos históricos, resuma comportamientos, identifique anomalías y proporcione alertas, con el objetivo de ser adoptado como una herramienta eficaz en los flujos operativos de Electro Dunas. 


## Características

El tablero de control tiene como objetivo el análisis y detección de anomalías en el comportamiento del consumo de energía de los clientes no regulados propios y terceros de ElectroDunas. Esta herramienta facilita la visualización del consumo histórico, la detección de anomalías y la predicción de comportamientos futuros, permitiendo una gestión más eficiente y proactiva del suministro eléctrico.

### Datos utilizados:
*	Periodo disponible: Desde el 1 de enero de 2021 hasta el 1 de abril de 2023.
*	Variables: Energía activa (kWh), energía reactiva (kVarh), Sector económico e ID cliente.
*	Cantidad de clientes: 15 clientes analizados con alta completitud de datos (≥ 99%).

### Metodología – Modelos
*	Detección de anomalías: implementación de modelos no supervisados y series de tiempo tales como DBSCAN y KernelCPD.
*	Predicción consumo: SVR (Support Vector Regression) y LSTM (Long Short-Term Memory)
*	Clasificación anomalías futuras: Random Forest y Gradient Boosting

### Interactividad y Funcionalidad
*	Filtros Dinámicos: Permiten explorar y segmentar los datos según diferentes criterios tales como el sector económico, intervalo de tiempo (fecha inicio y fecha fin), ID cliente, nivel de confianza del pronóstico y periodo de pronostico
*	Alertas de Anomalías: Notificaciones visuales cuando se detectan patrones de consumo atípicos tanto a nivel histórico como patrones futuros.
*	Cuadro resumen con la información de las anomalías detectadas según el periodo seleccionado con la información del registro exacto y su desviación.
  
## Repositorio

### Niveles
Cuatro carpetas principales
- informes: Prototipo Fachada, Tabla se requerimientos, Desarrollo y Prueba de los Modelos, Validación del prototipo con base en los requerimientos y Manual de Usuario
- src: Jupyter Notebooks
- satatics: Imagenes, versión minimizada del archivo de CSS de Bootstrap, versión minimizada del archivo JavaScript de jQuery, archivo JavaScript personalizado y archivo CSS personalizado
- templates: Plantilas Html de cada pagina

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


## Requerimientos Técnicos
* Linux or macOS or Windows
* bash
* version > python 3.5
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
