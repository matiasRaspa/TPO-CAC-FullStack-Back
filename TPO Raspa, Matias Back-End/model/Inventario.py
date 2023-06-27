from model.DataBase import get_db_connection
from flask import jsonify
from model.Producto import Producto

class Inventario:
    # Este método permite crear objetos de la clase "Producto" y agregarlos al inventario.
    def agregar_producto(self, producto):
        producto_existente = self.consultar_producto(producto.codigo)
        if producto_existente:
            return jsonify({'message': 'Ya existe un producto con ese código.'}), 400
        self.conexion = get_db_connection() # Conexión a la DB
        self.cursor = self.conexion.cursor() # Creo cursor
        sql = f'INSERT INTO productos VALUES ({producto.codigo}, "{producto.descripcion}", {producto.cantidad}, {producto.precio});'
        self.cursor.execute(sql)
        self.conexion.commit()
        self.cursor.close() # Cierro cursor
        self.conexion.close() # Cierro conexión a la DB
        return jsonify({'message': 'Producto agregado correctamente.'}), 200

    # Este método permite consultar datos de productos que están en el inventario
    # Devuelve el producto correspondiente al código proporcionado o False si no existe.
    def consultar_producto(self, codigo):
        self.conexion = get_db_connection() # Conexión a la DB
        self.cursor = self.conexion.cursor() # Creo cursor
        sql = f'SELECT * FROM productos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        self.cursor.close() # Cierro cursor
        self.conexion.close() # Cierro conexión a la DB
        if row:
            codigo, descripcion, cantidad, precio = row
            return Producto(codigo, descripcion, cantidad, precio)
        return None
    
    # Este método permite modificar datos de productos que están en el inventario
    # Utiliza el método consultar_producto del inventario y modificar del producto.
    def modificar_producto(self, producto):
        buscarProducto = self.consultar_producto(producto.codigo)
        if buscarProducto:
            self.conexion = get_db_connection() # Conexión a la DB
            self.cursor = self.conexion.cursor() # Creo cursor
            buscarProducto.modificar(producto.descripcion, producto.cantidad, producto.precio)
            sql = f'UPDATE productos SET descripcion = "{producto.descripcion}", cantidad = {producto.cantidad}, precio = {producto.precio} WHERE codigo = {buscarProducto.codigo};'
            self.cursor.execute(sql)
            self.conexion.commit()
            self.cursor.close() # Cierro cursor
            self.conexion.close() # Cierro conexión a la DB
            return jsonify({'message': 'Producto modificado correctamente.'}), 200
        return jsonify({'message': 'Producto no encontrado.'}), 404

    # Este método elimina el producto indicado por codigo de la lista mantenida en el inventario.
    def eliminar_producto(self, codigo):
        self.conexion = get_db_connection() # Conexión a la DB
        self.cursor = self.conexion.cursor() # Creo cursor
        sql = f'DELETE FROM productos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            self.cursor.close() # Cierro cursor
            self.conexion.close() # Cierro conexión a la DB
            return jsonify({'message': 'Producto eliminado correctamente.'}), 200
        self.cursor.close() # Cierro cursor
        self.conexion.close() # Cierro conexión a la DB
        return jsonify({'message': 'Producto no encontrado.'}), 404

    # Este método imprime en la terminal una lista con los datos de los productos que figuran en el inventario.
    def listar_productos(self):
        self.conexion = get_db_connection() # Conexión a la DB
        self.cursor = self.conexion.cursor() # Creo cursor
        listaProductos = []
        self.cursor.execute("SELECT * FROM productos")
        rows = self.cursor.fetchall()
        self.cursor.close() # Cierro cursor
        self.conexion.close() # Cierro conexión a la DB
        for row in rows:
            codigo, descripcion, cantidad, precio = row
            producto = {'codigo': codigo,
                        'descripcion': descripcion,
                        'cantidad': cantidad,
                        'precio': precio}
            listaProductos.append(producto)
        return jsonify(listaProductos), 200