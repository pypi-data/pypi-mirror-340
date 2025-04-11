class Precios:

    @staticmethod #metodo estatico dentro de una clase
    def calcular_precio_final(precio_base,impuesto,descuento):
        return precio_base + impuesto - descuento
    