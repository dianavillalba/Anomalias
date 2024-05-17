from flask import Flask, render_template
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots

df = pd.read_excel('clientes_anomalias.xlsx')
print(f'Datos Cargados: {df.shape}')

def obtener_informacion_cliente(df, id_cliente, fecha_ini='2021-01-01', fecha_fin='2023-03-31'):

        # Filtrar por el ID del cliente
    df_cliente = df[df['ID_Cliente'] == id_cliente]

    # Inicializar listas para almacenar los labels y los valores
    labels = []
    valores = []

    # Obtener la fecha mínima y máxima de la serie
    fecha_minima = df_cliente['Fecha'].min()
    fecha_maxima = df_cliente['Fecha'].max()

    # Filtrar por las fechas de inicio y fin si se proporcionan
    df_cliente = df_cliente[(df_cliente['Fecha'] >= fecha_ini) & (df_cliente['Fecha'] <= fecha_fin)]

    # Calcular el consumo total de energía activa y reactiva
    consumo_activa_total = df_cliente['Active_energy'].sum()
    consumo_reactiva_total = df_cliente['Reactive_energy'].sum()

    # Obtener el sector económico del cliente
    sector_economico = df_cliente.iloc[0]['Sector'] if not df_cliente.empty else None
    
    # Obtener la posicion en el ranking de anomalias actuales
    ranking_total = df.groupby('ID_Cliente')['Anomalies_final'].sum().sort_values()
    rank_anomalias = ranking_total.index.get_loc(id_cliente) + 1

    # Agregar los labels y valores a las listas correspondientes
    labels.extend(['Sector', 'Energía Activa', 'Energía Reactiva', 'Fecha Mínima', 'Fecha Máxima', 'Posición Ranking Anomalías Actuales'])
    valores.extend([sector_economico, consumo_activa_total, consumo_reactiva_total, fecha_minima, fecha_maxima, rank_anomalias])

    return labels, valores

# Ejemplo de uso de la función
id_cliente = 'Cliente 01'
labels, valores = obtener_informacion_cliente(df, id_cliente)

print("Información del Cliente:")
for label, valor in zip(labels, valores):
    print(f'{label}: {valor}')

def generar_grafica(df, id_cliente, metrica, fecha_ini='2021-01-01', fecha_fin='2023-03-31'):
    # Filtrar el DataFrame por el cliente_id especificado
    cliente_data = dataframe[dataframe['ID_Cliente'] == cid_cliente]

    # Filtrar por las fechas de inicio y fin si se proporcionan
    df_cliente = df_cliente[(df_cliente['Fecha'] >= fecha_ini) & (df_cliente['Fecha'] <= fecha_fin)]
    
    # Agrupar por año, mes, semana, día de la semana y cliente, y calcular la media de la energía activa
    grouped = cliente_data.groupby(['Año', 'Mes', 'Dia_Semana', 'ID_Cliente'])[metrica].mean().reset_index()

    # Crear un diccionario para asignar un color a cada día de la semana
    colores_dias = {'Monday': 'blue', 'Tuesday': 'green', 'Wednesday': 'orange', 'Thursday': 'red', 'Friday': 'purple', 'Saturday': 'brown', 'Sunday': 'gray'}

    # Crear un objeto de trama Plotly
    fig = make_subplots()

    # Agregar cada serie de datos al gráfico
    for dia, color in colores_dias.items():
        dia_data = grouped[grouped['Dia_Semana'] == dia]
        if not dia_data.empty:
            fig.add_trace(go.Scatter(x=dia_data.index, y=dia_data[metrica], mode='lines+markers', name=dia, line=dict(color=color)))

    # Establecer el diseño del gráfico
    fig.update_layout(title=f'Energía Activa por Período - Cliente {id_cliente}', xaxis_title='Period', yaxis_title= metrica, legend_title='Día de la Semana', showlegend=True)

    # Guardar la figura en un archivo HTML
    ruta_grafica = f'static/cliente_{id_cliente}_energia_por_periodo.html'
    fig.write_html(ruta_grafica)

    return ruta_grafica



app = Flask(__name__, static_url_path='/static')

current_date = datetime.now().strftime("%Y/%m/%d")

@app.route('/')
def home():
    return render_template('index.html', current_page='home', current_date=current_date)

@app.route('/perfil')
def perfil():
    return render_template('perfil.html', current_page='perfil', current_date=current_date)

@app.route('/anomalias')
def anomalias():
    return render_template('anomalias.html', current_page='anomalias', current_date=current_date)

@app.route('/ficha')
def ficha():
    return render_template('ficha.html', current_page='ficha', current_date=current_date)

if __name__ == '__main__':
    app.run(debug=True)