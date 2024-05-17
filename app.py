from flask import Flask, render_template,request
from datetime import datetime
import pandas as pd
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import seaborn as sns
import squarify
import matplotlib.ticker as ticker
import textwrap

df = pd.read_excel('clientes_anomalias.xlsx')
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Año'] = df['Fecha'].dt.year
df['Mes'] = df['Fecha'].dt.month
df['Dia_Semana'] = df['Fecha'].dt.day_name()
df['Hora'] = df['Fecha'].dt.hour

print(f'Datos Cargados: {df.shape}')

def filtrar_cliente(df,id_cliente, fecha_ini, fecha_fin ):

    df_cliente = df[df['ID_Cliente'] == id_cliente]
    df_cliente = df_cliente[(df_cliente['Fecha'] >= fecha_ini) & (df_cliente['Fecha'] <= fecha_fin)]
    df_cliente = df_cliente['tipo'] = 'actual'
    return  df_cliente 

def filtrar_fechas(pagina, df, fecha_ini, fecha_fin ):

    df_fechas = df[(df['Fecha'] >= fecha_ini) & (df['Fecha'] <= fecha_fin)]

    return df_fechas 

def obtener_posicion_ranking_anomalias(df, id_cliente, fecha_ini, fecha_fin,tipo):

    df_cliente = df[df['ID_Cliente'] == id_cliente]
    df_cliente = df_cliente[(df_cliente['Fecha'] >= fecha_ini) & (df_cliente['Fecha'] <= fecha_fin)]

    # Filtrar por el tipo de dato actual o pronostico
    df_cliente = df_cliente[df_cliente['Tipo'] == tipo]

    # Verificar si el DataFrame está vacío después del filtrado
    if df_cliente.empty:
        return 0
  
    # Calcular el ranking total de anomalías por cliente
    ranking_total = df.groupby('ID_Cliente')['Anomalies_final'].sum().sort_values(ascending=False)
    
    # Convertir el ranking_total en un DataFrame y resetear el índice para tener un índice numérico
    ranking_df = ranking_total.reset_index()
    
    # Agregar una columna de ranking basado en el índice (que está ordenado)
    ranking_df['Rank'] = ranking_df.index + 1
    
    # Verificar si el cliente existe en el ranking
    if len(ranking_df[ranking_df['ID_Cliente'] == id_cliente]) > 0:
        rank_anomalias = ranking_df[ranking_df['ID_Cliente'] == id_cliente]['Rank'].values[0]
    else:
        rank_anomalias = None
    
    return rank_anomalias


def obtener_numero_anomalias(df, id_cliente, fecha_ini, fecha_fin, tipo):

    df_cliente = df[df['ID_Cliente'] == id_cliente]
    df_cliente = df_cliente[(df_cliente['Fecha'] >= fecha_ini) & (df_cliente['Fecha'] <= fecha_fin)]

   # Filtrar por el tipo de dato actual o pronostico
    df_cliente = df_cliente[df_cliente['Tipo'] == tipo]

    # Verificar si el DataFrame está vacío después del filtrado
    if df_cliente.empty:
        return 0

    # Contar el número de anomalías
    numero_anomalias = df_cliente['Anomalies_final'].sum()

    return numero_anomalias


def info_perfil(pagina, df, id_cliente, fecha_ini, fecha_fin):

        # Filtrar por el ID del cliente
    df_cliente = df[df['ID_Cliente'] == id_cliente]

    labels = []
    valores = []

    # Obtener la fecha mínima y máxima de la serie
    fecha_minima = df_cliente['Fecha'].min()
    fecha_maxima = df_cliente['Fecha'].max()

    df_cliente = df_cliente[(df_cliente['Fecha'] >= fecha_ini) & (df_cliente['Fecha'] <= fecha_fin)]

    # Calcular el consumo total de energía activa y reactiva
    consumo_activa_total = df_cliente['Active_energy'].sum()
    consumo_reactiva_total = df_cliente['Reactive_energy'].sum()

    # Obtener el sector económico del cliente
    sector_economico = df_cliente.iloc[0]['Sector'] if not df_cliente.empty else None
      
    # Agregar los labels y valores a las listas correspondientes
    labels.extend(['Sector', 'Total Energía Activa', 'Total Energía Reactiva', 'Información Disponible Desde', 'Información Disponible Hasta'])
    valores.extend([sector_economico, consumo_activa_total, consumo_reactiva_total, fecha_minima, fecha_maxima])

    return labels, valores


def info_anomalias(pagina, df, id_cliente, fecha_ini, fecha_fin):

    df_cliente = df[df['ID_Cliente'] == id_cliente]
    df_cliente = df_cliente[(df_cliente['Fecha'] >= fecha_ini) & (df_cliente['Fecha'] <= fecha_fin)]

    labels = []
    valores = []

    consumo_activa_total = df_cliente['Active_energy'].sum()
    consumo_reactiva_total = df_cliente['Reactive_energy'].sum()

    sector_economico = df_cliente.iloc[0]['Sector'] if not df_cliente.empty else None
    
    rank_anomalias = obtener_posicion_ranking_anomalias(df, id_cliente, fecha_ini, fecha_fin,'actual')
    anomalias_actuales = obtener_numero_anomalias(df, id_cliente, fecha_ini, fecha_fin, 'actual')
    anomalias_pronosticadas = obtener_numero_anomalias(df, id_cliente, fecha_ini, fecha_fin, 'pronostico')

    # Agregar los labels y valores a las listas correspondientes
    labels.extend(['Sector', 'Total Energía Activa', 'Total Energía Reactiva', 'Posición Ranking Anomalías', 'Cantidad de anomalías detectadas actuales', 'Cantidad de anomalías detectadas proyectadas'])
    valores.extend([sector_economico, consumo_activa_total, consumo_reactiva_total, rank_anomalias, anomalias_actuales, anomalias_pronosticadas ])

    return labels, valores

def lista_anomalias_cliente(df, cliente_id, fecha_inicio, fecha_fin, tipo):

    df_cliente = df[df['ID_Cliente'] == cliente_id]
    df_cliente = df_cliente[(df_cliente['Fecha'] >= fecha_inicio) & (df_cliente['Fecha'] <= fecha_fin)]
    df_cliente = df_cliente[df_cliente['Tipo'] == tipo]
    df_cliente = df_cliente[df_cliente['Anomalies_final'] == 1]

    # Verificar si el DataFrame está vacío después del filtrado
    if df_cliente.empty:
        return "No se encontraron anomalías en el rango de fechas."

    # Ordenar por fecha en orden descendente y seleccionar las 10 más recientes
    df_cliente = df_cliente.sort_values(by='Fecha', ascending=False).head(10)

    # Generar el texto para las anomalías
    lista_anomalias = []
    for _, row in df_cliente.iterrows():
        anomalia_texto = f"Fecha y Hora: {row['Fecha']} Energia Activa: {row['Active_energy']}"
        lista_anomalias.append(anomalia_texto)

    # Unir las anomalías en un solo texto separado por \n
    texto_anomalias = "\n".join(lista_anomalias)

    return texto_anomalias

def plot_average_by_day_of_week(df, cliente_id, fecha_inicial, fecha_final, variable):

    # Capitalizar los nombres de los días en el DataFrame para que coincidan con la lista weekdays
    df['Dia_Semana'] = df['Dia_Semana'].str.capitalize()

    # Group by day of the week, year, and month and calculate the average value
    grouped = df.groupby(['Año', 'Mes', 'Dia_Semana'])[variable].mean().reset_index()

    # Create a list of weekdays in the order you want them to appear on the plot
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    imagenes_base64 = ""

    # Plot one line for each day of the week
    plt.figure(figsize=(12, 8))

    for day_of_week, day_name in enumerate(weekdays):  # Usamos enumerate para obtener el índice y el nombre del día
        # Filter data for the current day of the week
        day_data = grouped[grouped['Dia_Semana'] == day_name]

        # Plot the average value for the current day of the week
        plt.plot(range(len(day_data)), day_data[variable], marker='o', linestyle='-', label=day_name)

    plt.title(f'{cliente_id}; Periodo: {fecha_inicial} - {fecha_final}; Promedio de {variable} por dia de la semana y mes')
    plt.xlabel('Period')
    plt.ylabel('Average Value')
    plt.xticks(range(len(day_data)), [f'{y}-{m:02}' for y, m in zip(day_data['Año'], day_data['Mes'])], rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()


    # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Añadir la imagen base64 a la lista
    imagenes_base64 = data_uri

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return imagenes_base64

def plot_heatmap_energy_by_hour_and_day(df, cliente_id, fecha_inicial, fecha_final, variable):
      
    # Crear tabla pivote con los datos filtrados
    pivot_table = df.pivot_table(index='Hora', columns='Dia_Semana', values=variable, aggfunc='mean')

    # Ordenar los días de la semana dentro de la tabla pivote
    pivot_table = pivot_table.reindex(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    imagenes_base64 = ""
    
    # Crear el mapa de calor
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, cmap='YlGnBu')
    plt.title(f'{cliente_id}; Periodo: {fecha_inicial} - {fecha_final}; {variable} - Mapa de calor por hora y dia de la semana')
    plt.xlabel('Día de la Semana')
    plt.ylabel('Hora del día')
    plt.xticks(rotation=0)
    plt.tight_layout()
 
    # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Añadir la imagen base64 a la lista
    imagenes_base64 = data_uri

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return imagenes_base64

def plot_line_time_series(df, cliente_id, fecha_inicial, fecha_final, variable):

    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df_sorted = df.sort_values('Fecha')  # Ordenar el DataFrame por la columna 'Fecha'

    imagenes_base64 = ""

    plt.figure(figsize=(12, 8))

    plt.plot(df_sorted['Fecha'], df_sorted[variable], color='blue')
    plt.xlabel('Fecha')
    plt.ylabel(f'Consumo de {variable}')
    plt.title(f'{cliente_id}; Periodo: {fecha_inicial} - {fecha_final}; Consumo de {variable}')
    plt.legend()
    plt.xticks(rotation=45)  # Rotar etiquetas del eje x
    plt.tight_layout()

    # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Añadir la imagen base64 a la lista
    imagenes_base64 = data_uri

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return imagenes_base64

def plot_average_by_month(df, cliente_id, fecha_inicio, fecha_fin, variable):
    
    # Group by year and month and calculate the average value
    grouped = df.groupby(['Año', 'Mes'])[variable].mean().reset_index()

    imagenes_base64 = ""

    # Plot the average value for each month
    plt.figure(figsize=(12, 8))
    
    # Plot the average value for each month
    plt.plot(range(len(grouped)), grouped[variable], marker='o', linestyle='-')
    
    plt.title(f'{cliente_id}; Periodo: {fecha_inicio} - {fecha_fin}; Promedio de {variable} por mes')
    plt.xlabel('Period')
    plt.ylabel('Average Value')
    plt.xticks(range(len(grouped)), [f'{y}-{m:02}' for y, m in zip(grouped['Año'], grouped['Mes'])], rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Añadir la imagen base64 a la lista
    imagenes_base64 = data_uri

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return imagenes_base64


def plot_boxplot_by_month(df, cliente_id, fecha_inicio, fecha_fin, variable):
  
    # Convertir las columnas de año y mes en un solo periodo
    df['Periodo'] = df.apply(lambda row: f"{row['Año']}-{row['Mes']:02}", axis=1)
  
    imagenes_base64 = ""  
    # Preparar los datos para el boxplot
    data = [df[df['Periodo'] == period][variable].values for period in sorted(df['Periodo'].unique())]
    
    # Plot the boxplot
    plt.figure(figsize=(12, 8))
    plt.boxplot(data, labels=sorted(df['Periodo'].unique()), patch_artist=True)

    plt.title(f'{cliente_id}; Periodo: {fecha_inicio} - {fecha_fin}; Distribución de {variable} por mes')
    plt.xlabel('Period')
    plt.ylabel(variable)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    
    # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Añadir la imagen base64 a la lista
    imagenes_base64 = data_uri

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return imagenes_base64


def plot_total_and_yoy_variance_by_year(df, fecha_inicio, fecha_fin, variable):
   
    # Asegurarse de que la columna 'Año' está en el DataFrame
    df['Año'] = pd.to_datetime(df['Fecha']).dt.year
    
    imagenes_base64 = ""  

    # Agrupar los datos por año y calcular el total de la variable
    total_by_year = df.groupby('Año')[variable].sum().reset_index()
    
    # Calcular la variación YoY
    total_by_year['YoY_Variance'] = total_by_year[variable].pct_change() * 100

    # Plot the total information by year as bars
    fig, ax1 = plt.subplots(figsize=(6, 4))

    ax1.bar(total_by_year['Año'], total_by_year[variable], color='#005c99', label='Total')
    ax1.set_xlabel('Año')
    ax1.set_ylabel(f'{variable}')
    ax1.tick_params(axis='y')
    ax1.set_xticks(total_by_year['Año'])  # Set the x-axis ticks to be the years as integers
    
    # Create a second y-axis for the YoY variance
    ax2 = ax1.twinx()
    ax2.plot(total_by_year['Año'], total_by_year['YoY_Variance'], color='orange', marker='o', linestyle='-', label='% Varianza Año Anterior')
    ax2.set_ylabel('Varianza Año Anterior (%)')
    ax2.tick_params(axis='y')

    # Adding title and grid
    plt.title(f'{variable}', pad=20)
    ax1.grid(True,linestyle='--', alpha=0.7)
    fig.tight_layout()

    # Adding legends
    ax1.legend(loc='upper left', bbox_to_anchor=(0.02, 1.08), borderaxespad=0, frameon=False)
    ax2.legend(loc='upper right', bbox_to_anchor=(0.98, 1.08), borderaxespad=0, frameon=False)


    # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Añadir la imagen base64 a la lista
    imagenes_base64 = data_uri

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return imagenes_base64

def plot_clientes_yoy_variance(df, fecha_inicio, fecha_fin):
    
    # Asegurarse de que la columna 'Año' está en el DataFrame
    df['Año'] = pd.to_datetime(df['Fecha']).dt.year
    
    imagenes_base64 = ""  

    # Agrupar los datos por año y calcular el número de clientes únicos
    total_by_year = df.groupby('Año')['ID_Cliente'].nunique().reset_index(name='Num_Clientes')
    
    # Calcular la variación YoY
    total_by_year['YoY_Variance'] = total_by_year['Num_Clientes'].pct_change() * 100

    # Plot the total information by year as bars
    fig, ax1 = plt.subplots(figsize=(6, 4))

    ax1.bar(total_by_year['Año'], total_by_year['Num_Clientes'], color='#005c99', label='Total Clientes')
    
    ax1.set_xlabel('Año')
    ax1.set_ylabel('#Clientes')
    ax1.tick_params(axis='y')
    ax1.set_xticks(total_by_year['Año'])  # Set the x-axis ticks to be the years as integers
    
    # Create a second y-axis for the YoY variance
    ax2 = ax1.twinx()
    ax2.plot(total_by_year['Año'], total_by_year['YoY_Variance'], color='orange', marker='o', linestyle='-', label='% Varianza Año Anterior')
    ax2.set_ylabel('Varianza Año Anterior (%)')

    ax2.tick_params(axis='y')

    # Adding title and grid
    plt.title('Clientes', pad=20)
    ax1.grid(True, linestyle='--', alpha=0.7)

    fig.tight_layout()

    # Adding legends
    ax1.legend(loc='upper left', bbox_to_anchor=(0.02, 1.08), borderaxespad=0, frameon=False)
    ax2.legend(loc='upper right', bbox_to_anchor=(0.98, 1.08), borderaxespad=0, frameon=False)


    # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Añadir la imagen base64 a la lista
    imagenes_base64 = data_uri

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return imagenes_base64


def plot_treemap_sector_clientes(df, fecha_inicial, fecha_final):
    # Count distinct clients within each sector
    sector_client_counts = df.groupby('Sector')['ID_Cliente'].nunique().sort_index()

    imagenes_base64 = ""

    # Create labels for sectors
    labels = [f"{sector}\n{count}" for sector, count in zip(sector_client_counts.index, sector_client_counts)]

    # Create sizes for sectors
    sizes = sector_client_counts.values

    # Create a treemap
    plt.figure(figsize=(7, 5))
    squarify.plot(sizes=sizes, label=labels, color=sns.color_palette("Paired", len(sector_client_counts)),
                  text_kwargs={'wrap': True })
    plt.title('Clientes por sector')

    # Remove axis
    plt.axis('off')

     # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Añadir la imagen base64 a la lista
    imagenes_base64 = data_uri

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return imagenes_base64

def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width, break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)


def plot_waterfall_anomalias(df, fecha_inicio, fecha_fin):
    # Agrupar los datos por sector y contar las anomalías
    sector_anomaly_counts = df.groupby('Sector')['Anomalies_final'].sum()

    # Ordenar los sectores por el número total de anomalías en orden descendente
    sector_anomaly_counts = sector_anomaly_counts.sort_values(ascending=False)

    # Calcular el porcentaje de cada sector con respecto al total
    total_anomalies = sector_anomaly_counts.sum()
    sector_percentages = (sector_anomaly_counts / total_anomalies) * 100

    # Crear un gráfico de barras vertical
    plt.figure(figsize=(7, 5))
    barras = plt.bar(sector_anomaly_counts.index, sector_anomaly_counts.values, color='lightblue')

    for i, barra in enumerate(barras):
        plt.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + 0.5, f'{sector_percentages.iloc[i]:.1f}%', ha='center', va='bottom')

    # Agregar etiquetas y título
    plt.ylabel('#Anomalías')
    plt.title('Anomalías por sector (Active_energy)')

    # Agregar líneas de cuadrícula
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Ajustar el diseño
    plt.tight_layout()

    # Llamar a la función wrap_labels para envolver los labels del eje x
    wrap_labels(plt.gca(), 25)

    # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return data_uri



def plot_top_anomaly_clients(df, fecha_inicio, fecha_fin):
    
    imagenes_base64 = ""  

    # Group data by client and count anomalies
    client_anomaly_counts = df.groupby('ID_Cliente')['Anomalies_final'].sum().sort_values(ascending=False)

    # Select the top 5 clients if there are at least 5 clients, otherwise select all clients
    top_clients = client_anomaly_counts.head(5) if len(client_anomaly_counts) >= 5 else client_anomaly_counts

    # Plotting the horizontal bar chart
    plt.figure(figsize=(7, 5))
    bars = plt.barh(top_clients.index, top_clients.values, color='#005c99')
    plt.xlabel('# Anomalías')
    #plt.ylabel('Client ID')
    plt.title('Top 5 clientes con mayor número de anomalías (Active_energy)')

    # Displaying the number of anomalies next to each bar
    for bar, count in zip(bars, top_clients.values):
        plt.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f'{count}', va='center')

    plt.gca().invert_yaxis()  # Invert y-axis to display the highest count at the top

   # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Añadir la imagen base64 a la lista
    imagenes_base64 = data_uri

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return imagenes_base64


def plot_anomalias_time_series(df, cliente_id, fecha_inicio, fecha_fin,variable):

    imagenes_base64 = ""

    df['Fecha'] = pd.to_datetime(df['Fecha'])
    plt.figure(figsize=(12, 8))
    plt.plot(df['Fecha'], df[variable], color='blue', label=variable)

    anomalies = df[df['Anomalies_descriptive'] == 1]
    plt.scatter(anomalies['Fecha'], anomalies[variable], color='red', label='Anomalías', zorder=5)
    plt.ylabel(f'{variable}')
    plt.title(f'Serie de Tiempo del Consumo de {variable}')
    plt.legend()

    plt.xticks(rotation=45)

    # Convertir la gráfica a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    # Añadir la imagen base64 a la lista
    imagenes_base64 = data_uri

    # Limpiar la figura actual para la siguiente iteración
    plt.clf()

    return imagenes_base64 


app = Flask(__name__, static_url_path='/static')

@app.context_processor
def inject_clients():
    # Define the variable you want to make available in the templates
    #clients = ['Cliente 01', 'Cliente 02', 'Cliente 10']
    clients = ['Cliente 01', 'Cliente 02', 'Cliente 03', 'Cliente 04', 'Cliente 05',
                'Cliente 06', 'Cliente 07', 'Cliente 08', 'Cliente 09', 'Cliente 10',
                'Cliente 16', 'Cliente 17', 'Cliente 18', 'Cliente 19', 'Cliente 20'] 

    # Return a dictionary containing the variable
    return {'clients': clients}

current_date = datetime.now().strftime("%Y/%m/%d")

@app.route('/')
def index():
    return render_template('index.html', current_page='index', current_date=current_date)

@app.route('/perfil')
def perfil():
    return render_template('perfil.html', current_page='perfil', current_date=current_date)

@app.route('/anomalias')
def anomalias():
    return render_template('anomalias.html', current_page='anomalias', current_date=current_date)

@app.route('/ficha')
def ficha():
    return render_template('ficha.html', current_page='ficha', current_date=current_date)

@app.route('/submitform', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Get form data
        form_fields = {}
        for field in request.form:
            form_fields[field] = request.form[field]

        pagina = request.form['pagina']
        fecha_inicial = request.form['fecha_inicial']
        fecha_final = request.form['fecha_final']
        
        tabla={'labels':None, 'valor':None }
        graficas = {}
        listas = {}

        if pagina == "index":
            
           df_fecha = filtrar_fechas(pagina, df, fecha_inicial, fecha_final)
           
           graficas['grafica1'] = plot_clientes_yoy_variance(df_fecha, '2021-01-01', '2023-03-31')
           graficas['grafica2'] = plot_total_and_yoy_variance_by_year(df_fecha, '2021-01-01', '2023-03-31' ,"Active_energy")
           graficas['grafica3'] = plot_total_and_yoy_variance_by_year(df_fecha, '2021-01-01', '2023-03-31' ,"Reactive_energy")
           graficas['grafica4'] = plot_treemap_sector_clientes(df_fecha, fecha_inicial,fecha_final)
           graficas['grafica5'] = plot_waterfall_anomalias(df_fecha, fecha_inicial,fecha_final)
           graficas['grafica6'] = plot_top_anomaly_clients(df_fecha, fecha_inicial,fecha_final)

        elif pagina == "perfil":
      
            id_cliente = request.form['cliente']
            tabla['labels'], tabla['valor']= info_perfil(pagina, df, id_cliente, fecha_inicial, fecha_final)
            df_cliente = filtrar_cliente(df,id_cliente, fecha_inicial, fecha_final)

            graficas['grafica1'] = plot_average_by_day_of_week(df_cliente,id_cliente, fecha_inicial, fecha_final, "Active_energy")
            graficas['grafica2'] = plot_average_by_month(df_cliente,id_cliente, fecha_inicial, fecha_final, "Active_energy")
            graficas['grafica3'] = plot_average_by_month(df_cliente,id_cliente, fecha_inicial, fecha_final, "Reactive_energy")
            graficas['grafica4'] = plot_heatmap_energy_by_hour_and_day(df_cliente,id_cliente, fecha_inicial, fecha_final, "Active_energy")
            graficas['grafica5'] = plot_boxplot_by_month(df_cliente,id_cliente, fecha_inicial, fecha_final, "Active_energy")
            graficas['grafica6'] = plot_boxplot_by_month(df_cliente,id_cliente, fecha_inicial, fecha_final, "Reactive_energy")

        elif pagina == "anomalias":

            id_cliente = request.form['cliente']
            df_cliente = filtrar_cliente(df,id_cliente, fecha_inicial, fecha_final)
            tabla['labels'], tabla['valor']= info_anomalias(pagina, df, id_cliente, fecha_inicial, fecha_final)

            graficas['grafica1'] = plot_anomalias_time_series(df_cliente,id_cliente, fecha_inicial, fecha_final, "Active_energy")
            graficas['grafica2'] = plot_anomalias_time_series(df_cliente,id_cliente, fecha_inicial, fecha_final, "Reactive_energy")
            listas['lista1'] = lista_anomalias_cliente(df_cliente,id_cliente, fecha_inicial, fecha_final, 'actual')
            listas['lista2'] = lista_anomalias_cliente(df_cliente,id_cliente, fecha_inicial, fecha_final, 'pronostico')
        else:
            print("otro")


        # Process the form data here, e.g., save to database
        # Then return the form data to the template
        return render_template(pagina + '.html', form_fields=form_fields,current_page = pagina, current_date=current_date, tabla = tabla , graficas = graficas,listas=listas)
    

if __name__ == '__main__':
    app.run(debug=True)