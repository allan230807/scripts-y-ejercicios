import statistics 
import random 
from herencia_activos import ActivoFinanciero, Cryptoactivo, Accion

class Portafolio:
    def __init__(self, nombre_portafolio):
        self.nombre_portafolio = nombre_portafolio
        self.activos = [] 

    def agregar_activo(self, activo):
        self.activos.append(activo)

    def simular_mercados(self, dias, media, volatilidad):
        for activo in self.activos:
            activo.simulacion_rendimientos(
                dias, media, volatilidad
            )
    def calcular_valor_total(self):
        total = 0.0 
        for activo in self.activos:
            total += activo.precio_actual
        return total 

    def mostrar_resumen(self):
        print(f"\n==================================================")
        print(f"📊 REPORT DE PORTAFOLIO: {self.nombre_portafolio.upper()}")
        print(f"==================================================")

        if not self.activos:
            print("⚠️ El portafolio no contiene activos registrados.")
            return

        for i, activo in enumerate(self.activos, 1):
            print(f"[{i}] {activo}")

        print(f"--------------------------------------------------")
        print(
            f"💰 VALOR TOTAL DEL PORTAFOLIO: ${self.calcular_valor_total():,.2f}"
        )
        print(f"==================================================\n")

if __name__ == "__main__":
    # 1. Instanciamos el portafolio
    mi_fondo = Portafolio("Fondo Alpha Quant")

    # 2. Agregamos activos de distintos tipos (Polimorfismo)
    mi_fondo.agregar_activo(Accion("AAPL", 220.0, dividendo_anual=2.0))
    mi_fondo.agregar_activo(Accion("NVDA", 120.0, dividendo_anual=0.15))
    mi_fondo.agregar_activo(Cryptoactivo("BTC", 65000.0, comision_red=0.001))
    mi_fondo.agregar_activo(Cryptoactivo("ETH", 3400.0, comision_red=0.0015))

    print("--- INICIO DE JORNADA ---")
    mi_fondo.mostrar_resumen()

    # 3. Simulamos 30 días de mercado para todos los activos
    mi_fondo.simular_mercados(dias=30, media=0.001, volatilidad=0.02)

    print("--- TRAS 30 DÍAS DE SIMULACIÓN DE MERCADO ---")
    mi_fondo.mostrar_resumen()