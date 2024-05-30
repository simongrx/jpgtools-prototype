import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt

# Cargar los archivos CSV
clientes = pd.read_csv('csv/jpgclientes.csv')
compras = pd.read_csv('csv/jpgcompras.csv')
interacciones = pd.read_csv('csv/jpginteracciones.csv')
potenciales = pd.read_csv('csv/jpgpotenciales.csv')

# Poner etiquetas
clientes['es_cliente'] = 1
potenciales['es_cliente'] = 0

# Renombrar columnas para consistencia
clientes = clientes.rename(columns={'ID': 'ClienteID'})
potenciales = potenciales.rename(columns={'Empresa': 'ClienteID'})

# Convertir a string
clientes['ClienteID'] = clientes['ClienteID'].astype(str)
potenciales['ClienteID'] = potenciales['ClienteID'].astype(str)
compras['ClienteID'] = compras['ClienteID'].astype(str)
interacciones['ClienteID'] = interacciones['ClienteID'].astype(str)

# Mezclar los df de clientes y potenciales
datos_combinados = pd.concat([clientes, potenciales], ignore_index=True)

# Agregar datos de compras e interacciones
datos_combinados = datos_combinados.merge(compras.groupby('ClienteID').agg({'Total': 'sum', 'CompraID': 'count'}).rename(columns={'Total': 'TotalCompras', 'CompraID': 'NumCompras'}), on='ClienteID', how='left')
datos_combinados = datos_combinados.merge(interacciones.groupby('ClienteID').agg({'InteraccionID': 'count'}).rename(columns={'InteraccionID': 'NumInteracciones'}), on='ClienteID', how='left')

# Rellenar valores nulos con 0
datos_combinados[['TotalCompras', 'NumCompras', 'NumInteracciones']] = datos_combinados[['TotalCompras', 'NumCompras', 'NumInteracciones']].fillna(0)

# Selección de características y etiquetas
columnas_a_eliminar = ['ClienteID', 'es_cliente', 'Nombre', 'Email', 'Teléfono', 'Fecha', 'Contacto', 'Direccion', 'Ciudad', 'Pais']
columnas_a_eliminar_existentes = [col for col in columnas_a_eliminar if col in datos_combinados.columns]

X = datos_combinados.drop(columns=columnas_a_eliminar_existentes)
y = datos_combinados['es_cliente']

# One-hot encoding
X = pd.get_dummies(X)

# Imputar valores
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Convertir de nuevo a df
X = pd.DataFrame(X, columns=pd.get_dummies(datos_combinados.drop(columns=columnas_a_eliminar_existentes)).columns)

# Dividir datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Entrenar modelo
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predicciones
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluación del modelo
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Predecir la probabilidad de que las empresas potenciales se conviertan en clientes
columnas_a_eliminar_existentes_potenciales = [col for col in columnas_a_eliminar if col in potenciales.columns]
potenciales_X = pd.get_dummies(potenciales.drop(columns=columnas_a_eliminar_existentes_potenciales))
potenciales_X = potenciales_X.reindex(columns=X_train.columns, fill_value=0)
potenciales_X = imputer.transform(potenciales_X)

# Convertir de nuevo a df después de imputación
potenciales_X = pd.DataFrame(potenciales_X, columns=X_train.columns)

potenciales['probabilidad'] = model.predict_proba(potenciales_X)[:, 1]

# Exportar resultados
potenciales.to_csv('results/resultados_prediccion_clientes.csv', index=False)

print("Predicciones completadas. Resultados exportados.")

# Visualización de los resultados
resultados = pd.read_csv('results/resultados_prediccion_clientes.csv')

# Verificar si las columnas necesarias están presentes
if 'ClienteID' in resultados.columns and 'probabilidad' in resultados.columns:
    # Gráfico de barras
    plt.figure(figsize=(12, 8))
    resultados_ordenados = resultados.sort_values(by='probabilidad', ascending=False)
    resultados_ordenados.plot(kind='bar', x='ClienteID', y='probabilidad', legend=False)
    plt.title('Probabilidad de Compra de Empresas Potenciales - Barras', fontsize=14)
    plt.xlabel('ID de Empresa Potencial', fontsize=10)
    plt.ylabel('Probabilidad de Compra', fontsize=10)
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(fontsize=10)
    plt.savefig('data/probabilidad_compra_empresas_potenciales_barras.png')
    plt.close()
    print("Gráfico de barras guardado como 'data/probabilidad_compra_empresas_potenciales_barras.png'")
    
    # Gráfico de dispersión
    plt.figure(figsize=(12, 8))
    plt.scatter(resultados_ordenados['ClienteID'], resultados_ordenados['probabilidad'], alpha=0.5)
    plt.title('Probabilidad de Compra de Empresas Potenciales - Dispersión', fontsize=14)
    plt.xlabel('ID de Empresa Potencial', fontsize=10)
    plt.ylabel('Probabilidad de Compra', fontsize=10)
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(fontsize=10)
    plt.savefig('data/probabilidad_compra_empresas_potenciales_dispersion.png')
    plt.close()
    print("Gráfico de dispersión guardado como 'data/probabilidad_compra_empresas_potenciales_dispersion.png'")
else:
    print("Columnas necesarias para las gráficas de probabilidad de compra no se encuentran.")
