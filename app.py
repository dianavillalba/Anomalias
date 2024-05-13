from flask import Flask, render_template
from datetime import datetime
import pandas as pd
import numpy as np


df = pd.read_excel('clientes_anomalias.xlsx')
print(f'Datos Cargados: {df.shape}')

def obtener_informacion_cliente(df, id_cliente, fecha_ini='2022-01-01', fecha_fin='2023-03-31'):

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
    if fecha_ini == fecha_minima.strftime('%Y-%m-%d') and fecha_fin == fecha_maxima.strftime('%Y-%m-%d'):
        rank_anomalias = df_cliente.iloc[0]['Rank_anomalies'] if not df_cliente.empty else None
    else:
        # Calcular el ranking de todos los clientes basado en la suma de la columna 'Anomalies_final'
        ranking_total = df.groupby('ID_Cliente')['Anomalies_final'].sum().sort_values()

        # Obtener el ranking del cliente
        rank_anomalias = ranking_total.index.get_loc(id_cliente) + 1

        print(f'Las fechas de entrada no coinciden con las fechas mínima y máxima del DataFrame: {rank_anomalias}')
    
    # Agregar los labels y valores a las listas correspondientes
    labels.extend(['Sector', 'Energía Activa', 'Energía Reactiva', 'Fecha Mínima', 'Fecha Máxima', 'Posición Ranking Anomalías Actuales'])
    valores.extend([sector_economico, consumo_activa_total, consumo_reactiva_total, fecha_minima, fecha_maxima, rank_anomalias])

    return labels, valores

# Ejemplo de uso de la función
id_cliente = 'Cliente 10'
labels, valores = obtener_informacion_cliente(df, id_cliente)

print("Información del Cliente:")
for label, valor in zip(labels, valores):
    print(f'{label}: {valor}')

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