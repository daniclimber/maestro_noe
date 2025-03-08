import pandas as pd

#EXTRACT
df = pd.read_csv('dataset_ganancias.csv')

#TRANSFORM
# Primero, revisamos cuántos duplicados hay
duplicates = df.duplicated(subset=['id_usuario', 'dia_ganancias'], keep=False)
print(f'Total de duplicados: {duplicates.sum()}')

df_unique = df.drop_duplicates(subset=['id_usuario', 'dia_ganancias'], keep='first')
print(f'Se eliminaron {duplicates.sum()} duplicados')

# Convertir la columna 'date' a datetime si aún no lo es
df['dia_ganancias'] = pd.to_datetime(df['dia_ganancias'])

# Extraer el año y mes de la columna de fecha
df['year_month'] = df['dia_ganancias'].dt.to_period('Y')

# Agrupar por 'user_id' y 'year_month', y sumar las ganancias
grouped = df.groupby(['id_usuario', 'year_month'])[['ganancias_MXN', 'ganancias_USD', 'ganancias_CAD', 'ganancias_EUR']].sum().reset_index()
print('Se agrupo por usuario y año')


grouped['ganancias_MXN'] = grouped['ganancias_MXN'] * 1
grouped['ganancias_USD'] = grouped['ganancias_USD'] * 18.23250417
grouped['ganancias_CAD'] = grouped['ganancias_CAD'] * 13.31770667
grouped['ganancias_EUR'] = grouped['ganancias_EUR'] * 19.65434625

grouped['ganancia_total_MXN'] = grouped['ganancias_MXN'] + grouped['ganancias_USD'] + grouped['ganancias_CAD'] + grouped['ganancias_EUR']

grouped = grouped.drop(columns=['ganancias_MXN', 'ganancias_USD', 'ganancias_CAD', 'ganancias_EUR'], axis=1)
print('Se sumaron las ganancias ya convertidas a mxn')

#LOAD
grouped.to_csv('ganancias_mxn_portafolios.csv')