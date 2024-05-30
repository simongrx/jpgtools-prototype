import pandas as pd

clientes_columns = ['ID', 'Nombre', 'Empresa', 'Tipo', 'Sector', 'Tamaño', 'Ubicación', 'Email', 'Teléfono', 'Fecha']
compras_columns = ['CompraID', 'ClienteID', 'ProductoID', 'Fecha', 'Cantidad', 'Total']
interacciones_columns = ['InteraccionID', 'ClienteID', 'TipoInteraccion', 'Fecha', 'Detalle']
potenciales_columns = ['Empresa', 'Contacto', 'Sector', 'Empleados', 'Tamaño', 'Direccion', 'Ciudad', 'Pais', 'Telefono', 'Email']
preferencias_columns = ['PreferenciaID', 'ClienteID', 'Preferencia', 'Nivel']
productos_columns = ['ProductoID', 'Nombre', 'Categoria', 'Descripcion', 'Precio']

clientes = pd.read_csv('clientes.csv', header=None, names=clientes_columns)
compras = pd.read_csv('compras.csv', header=None, names=compras_columns)
interacciones = pd.read_csv('interacciones.csv', header=None, names=interacciones_columns)
potenciales = pd.read_csv('potenciales.csv', header=None, names=potenciales_columns)
preferencias = pd.read_csv('preferencias.csv', header=None, names=preferencias_columns)
productos = pd.read_csv('productos.csv', header=None, names=productos_columns)

clientes.to_csv('csv/jpgclientes.csv', index=False)
compras.to_csv('csv/jpgcompras.csv', index=False)
interacciones.to_csv('csv/jpginteracciones.csv', index=False)
potenciales.to_csv('csv/jpgpotenciales.csv', index=False)
preferencias.to_csv('csv/jpgpreferencias.csv', index=False)
productos.to_csv('csv/jpgproductos.csv', index=False)

print("Archivos CSV actualizados con encabezados correctamente.")
