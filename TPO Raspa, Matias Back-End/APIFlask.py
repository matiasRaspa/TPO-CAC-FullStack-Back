from model.DataBase import create_database, get_db_connection
from flask import Flask, jsonify, request
from flask_cors import CORS
from model.Producto import Producto
from model.Inventario import Inventario
from model.Carrito import Carrito
import atexit

# Crear la base de datos y la tabla si no existen
create_database()

# Función para limpiar la base de datos
def limpiar_base_de_datos():
    conexion = get_db_connection() # Conexión a la DB
    cursor = conexion.cursor() # Creo cursor
    cursor.execute("DELETE FROM productos")
    conexion.commit()
    cursor.close() # Cierro cursor
    conexion.close() # Cierro conexión a la DB

# Esta instancia representa nuestra aplicación Flask
app = Flask(__name__)
CORS(app)

# Crear una instancia de la clase Inventario
inventario = Inventario()

# Crear una instancia de la clase Carrito
carrito= Carrito()

# Ruta raiz
@app.route('/')
def index():
    return 'API de Inventario'

# Ruta para obtener la lista de productos del inventario
@app.route('/productos', methods=['GET'])
def obtener_productos():
    return inventario.listar_productos()

# Ruta para obtener los datos de un producto según su código
@app.route('/productos/<int:codigo>', methods=['GET'])
def obtener_producto(codigo):
    producto = inventario.consultar_producto(codigo)
    if producto:
        return jsonify({
            'codigo': producto.codigo,
            'descripcion': producto.descripcion,
            'cantidad': producto.cantidad,
            'precio': producto.precio
            }), 200
    return jsonify({'message': 'Producto no encontrado.'}), 404

# Ruta para agregar un producto al inventario
@app.route('/productos', methods=['POST'])
def agregar_producto():
        codigo = request.json.get('codigo')
        descripcion = request.json.get('descripcion')
        cantidad = request.json.get('cantidad')
        precio = request.json.get('precio')
        producto = Producto(codigo, descripcion, cantidad, precio)
        return inventario.agregar_producto(producto)

# Ruta para modificar un producto del inventario
@app.route('/productos/<int:codigo>', methods=['PUT'])
def modificar_producto(codigo):
        nueva_descripcion = request.json.get('descripcion')
        nueva_cantidad = request.json.get('cantidad')
        nuevo_precio = request.json.get('precio')
        producto = Producto(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio)
        return inventario.modificar_producto(producto)

# Ruta para eliminar un producto del inventario
@app.route('/productos/<int:codigo>', methods=['DELETE'])
def eliminar_producto(codigo):
    for item in carrito.items:
         if item.codigo == codigo:
              carrito.items.remove(item)
    return inventario.eliminar_producto(codigo)

# Ruta para obtener el contenido del carrito
@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    return carrito.mostrar()

# Ruta para agregar un producto al carrito
@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    return carrito.agregar(codigo, cantidad, inventario)

# Ruta para quitar un producto del carrito
@app.route('/carrito', methods=['DELETE'])
def quitar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    return carrito.quitar(codigo, cantidad)

# Registro del evento de cierre de la aplicación
atexit.register(limpiar_base_de_datos)

# Finalmente, si estamos ejecutando este archivo, lanzamos app.
if __name__ == '__main__':
    app.run()