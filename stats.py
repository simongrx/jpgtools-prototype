import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# cargar csv
clientes = pd.read_csv('csv/jpgclientes.csv')
compras = pd.read_csv('csv/jpgcompras.csv')
interacciones = pd.read_csv('csv/jpginteracciones.csv')
potenciales = pd.read_csv('csv/jpgpotenciales.csv')
preferencias = pd.read_csv('csv/jpgpreferencias.csv')
productos = pd.read_csv('csv/jpgproductos.csv')

# ver las columnas
print("Columnas en el DataFrame clientes:", clientes.columns)
print("Columnas en el DataFrame compras:", compras.columns)
print("Columnas en el DataFrame interacciones:", interacciones.columns)
print("Columnas en el DataFrame potenciales:", potenciales.columns)
print("Columnas en el DataFrame preferencias:", preferencias.columns)
print("Columnas en el DataFrame productos:", productos.columns)

# stats de interacciones
interacciones_summary = interacciones.describe()
interacciones_summary.to_csv('results/estadisticas_interacciones.csv', index=False)

# segmentación de perfiles de usuario
if 'Sector' in clientes.columns and 'ID' in clientes.columns:
    clientes_segmentados = clientes.groupby('Sector').agg(cantidad=('ID', 'count')).reset_index()
    clientes_segmentados.to_csv('results/segmentacion_perfil_usuario.csv', index=False)
else:
    print("La columna 'Sector' o 'ID' no se encuentra en el DataFrame clientes.")

# productos más populares
if 'ProductoID' in compras.columns and 'Cantidad' in compras.columns:
    productos_populares = compras.groupby('ProductoID').agg({'Cantidad': 'sum'}).sort_values(by='Cantidad', ascending=False).head(10)
    productos_populares = productos_populares.merge(productos, left_on='ProductoID', right_on='ProductoID')
    productos_populares.to_csv('results/productos_mas_populares.csv', index=False)
else:
    print("La columna 'ProductoID' o 'Cantidad' no se encuentra en el DataFrame compras.")

# visualizaciones
# interacciones por tipo
if 'TipoInteraccion' in interacciones.columns:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=interacciones, x='TipoInteraccion')
    plt.title('Interacciones por Tipo')
    plt.xlabel('Tipo de Interacción')
    plt.ylabel('Cantidad')
    plt.savefig('data/interacciones_por_tipo.png')
    plt.close()
else:
    print("La columna 'TipoInteraccion' no se encuentra en el DataFrame interacciones.")

# compras por segmento
if 'Sector' in clientes.columns and 'ClienteID' in compras.columns and 'Cantidad' in compras.columns:
    compras_segmento = compras.merge(clientes, left_on='ClienteID', right_on='ID').groupby('Sector').agg({'Cantidad': 'sum'}).reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=compras_segmento, x='Sector', y='Cantidad')
    plt.title('Compras por Sector')
    plt.xlabel('Sector')
    plt.ylabel('Cantidad')
    plt.savefig('data/compras_por_segmento.png')
    plt.close()
else:
    print("Las columnas necesarias para el análisis de compras por segmento no se encuentran en los DataFrames compras o clientes.")

# graficas de torta para segmentación de perfiles de usuario
segmentacion_perfil_usuario = pd.read_csv('results/segmentacion_perfil_usuario.csv')
if 'Sector' in segmentacion_perfil_usuario.columns and 'cantidad' in segmentacion_perfil_usuario.columns:
    plt.figure(figsize=(10, 6))
    segmentacion_perfil_usuario.set_index('Sector')['cantidad'].plot(kind='pie', autopct='%1.1f%%')
    plt.title('Segmentación de Perfiles de Usuario')
    plt.ylabel('')  # Eliminar la etiqueta del eje y
    plt.savefig('data/segmentacion_perfil_usuario_pie.png')
    plt.close()
else:
    print("Columnas necesarias para la gráfica de torta de segmentación de perfiles de usuario no se encuentran.")

# graficas de torta para productos más populares
productos_mas_populares = pd.read_csv('results/productos_mas_populares.csv')
if 'Nombre' in productos_mas_populares.columns and 'Cantidad' in productos_mas_populares.columns:
    plt.figure(figsize=(10, 6))
    productos_mas_populares.set_index('Nombre')['Cantidad'].plot(kind='pie', autopct='%1.1f%%')
    plt.title('Productos Más Populares')
    plt.ylabel('')  # Eliminar la etiqueta del eje y
    plt.savefig('data/productos_mas_populares_pie.png')
    plt.close()
else:
    print("Columnas necesarias para la gráfica de torta de productos más populares no se encuentran.")

# guardar resúmenes
clientes.describe().to_csv('results/estadisticas_clientes.csv', index=False)
compras.describe().to_csv('results/estadisticas_compras.csv', index=False)
preferencias.describe().to_csv('results/estadisticas_preferencias.csv', index=False)
productos.describe().to_csv('results/estadisticas_productos.csv', index=False)
potenciales.describe().to_csv('results/estadisticas_potenciales.csv', index=False)

print("Análisis y visualización completados. Archivos exportados.")
