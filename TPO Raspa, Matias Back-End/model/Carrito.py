from model.DataBase import get_db_connection
from flask import jsonify
from model.Producto import Producto

class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.items = [] # Lista de items en el carrito (variable de clase)

    # Este método permite agregar productos del inventario al carrito.
    def agregar(self, codigo, cantidad, inventario):
        # Nos aseguramos que el producto esté en el inventario
        producto = inventario.consultar_producto(codigo)
        if producto is None:
            return jsonify({'message': 'El producto no existe.'}), 404
        # Verificamos que la cantidad en stock sea suficiente
        if producto.cantidad < cantidad:
            return jsonify({'message': 'Cantidad en stock insuficiente.'}), 400
        # Si existe y hay stock, vemos si ya existe en el carrito.
        for item in self.items:
            if item.codigo == codigo:
                item.cantidad += cantidad
                # Actualizamos la cantidad en el inventario
                self.conexion = get_db_connection() # Conexión a la DB
                self.cursor = self.conexion.cursor() # Creo cursor
                sql = f'UPDATE productos SET cantidad = cantidad - {cantidad} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                self.cursor.close() # Cierro cursor
                self.conexion.close() # Cierro conexión a la DB
                return jsonify({'message': 'Producto agregado al carrito correctamente.'}), 200
        # Si no existe en el carrito, lo agregamos como un nuevo item.
        nuevo_item = Producto(codigo, producto.descripcion, cantidad, producto.precio)
        self.items.append(nuevo_item)
        # Actualizamos la cantidad en el inventario
        self.conexion = get_db_connection() # Conexión a la DB
        self.cursor = self.conexion.cursor() # Creo cursor
        sql = f'UPDATE productos SET cantidad = cantidad - {cantidad} WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        self.cursor.close() # Cierro cursor
        self.conexion.close() # Cierro conexión a la DB
        return jsonify({'message': 'Producto agregado al carrito correctamente.'}), 200
    
# Este método quita unidades de un elemento del carrito, o lo elimina.
    def quitar(self, codigo, cantidad):
        for item in self.items:
            if item.codigo == codigo:
                if cantidad > item.cantidad:
                    return jsonify({'message': 'Cantidad a quitar mayor a la cantidad en el carrito.'}), 400
                item.cantidad -= cantidad
                if item.cantidad == 0:
                    self.items.remove(item)
                # Actualizamos la cantidad en el inventario
                self.conexion = get_db_connection() # Conexión a la DB
                self.cursor = self.conexion.cursor() # Creo cursor
                sql = f'UPDATE productos SET cantidad = cantidad + {cantidad} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                self.cursor.close() # Cierro cursor
                self.conexion.close() # Cierro conexión a la DB
                return jsonify({'message': 'Producto quitado del carrito correctamente.'}), 200
        # Si el bucle finaliza sin novedad, es que ese producto NO ESTA en el carrito.
        return jsonify({'message': 'El producto no se encuentra en el carrito.'}), 404
    
    # Este método imprime en la terminal la lista de productos en el carrito
    def mostrar(self):
        productos_carrito = []
        for item in self.items:
            producto = {'codigo': item.codigo,
                        'descripcion': item.descripcion,
                        'cantidad': item.cantidad,
                        'precio': item.precio}
            productos_carrito.append(producto)
        return jsonify(productos_carrito), 200