import unittest
from app_sales.gestor_ventas import GestorVentas
from app_sales.exceptions import ImpuestosInvalidError, DescuentoInvalidoError

class TestGestorSales(unittest.TestCase):

    def  test_calculo_precio_final(self):
        gestor=GestorVentas(100.0,0.05,0.10)
        self.assertEqual(gestor.calcular_precio_final(),95.0)

    def test_impuesto_invalido(self):
        with self.assertRaises(ImpuestosInvalidError):
            GestorVentas(100.0,1.5,0.10) 

    def test_descuento_invalido(self):
        with self.assertRaises(DescuentoInvalidoError):
            GestorVentas(100.00,0.05,1.5)

if __name__=="__main__":
    unittest.main()
#python -m unittest discover -s tests .... comando para realizar el test se debe ejecutar desde la raiz del proyecto
