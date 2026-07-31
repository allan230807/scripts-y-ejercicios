import statistics
import random

class ActivoFinanciero:
    def __init__(self,ticker, precio_actual):
        self.ticker = ticker
        self._precio_inicial = precio_actual
        self._precio_actual = precio_actual
        self._historial_pnl = []
    @property
    def precio_actual(self):
        """Permite consultar el precio actual pero no modificarlo directamente."""
        return self._precio_actual
    @precio_actual.setter
    def precio_actual(self, nuevo_precio):
        if nuevo_precio <= 0:
            print(f"❌ ERROR: El precio no puede ser <= 0 ({nuevo_precio}). Cambio rechazado.")
        else:
            self._precio_actual = nuevo_precio
    def registrar_rendimiento(self, rendimiento):
        self._historial_pnl.append(rendimiento)
        self.precio_actual *= 1 + rendimiento

    def simulacion_rendimientos(self, dias, media_diaria, volatilidad_diaria):
        for _ in range(dias):
            cambio = random.gauss(media_diaria, volatilidad_diaria)
            self.registrar_rendimiento(cambio)
    def obtener_rendimiento_acumulado(self):
            return(self._precio_actual - self._precio_inicial) / self._precio_inicial
    def calcular_desviacion(self):
        if len(self._historial_pnl) < 2:
            return 0.0
        return statistics.stdev(self._historial_pnl)

    def obtener_rendimiento_acumulado(self):
        return (
            self._precio_actual - self._precio_inicial
        ) / self._precio_inicial

    def __str__(self):
        rendimiento_pct = self.obtener_rendimiento_acumulado() * 100
        return f"Ticker: {self.ticker} | Precio Actual: ${self._precio_actual:,.2f} | Retorno: {rendimiento_pct:+.2f}%"


if __name__ == "__main__":
    activo = ActivoFinanciero("NQ100", 18000.0)
    activo.simulacion_rendimientos(252, 0.0004, 0.015)
    print("--- Estado Inicial del Activo ---")
    print(activo)

    print("\n--- Pruebas de Encapsulamiento ---")
    activo.precio_actual = -500.0
    print(f"Precio tras intromisión: ${activo.precio_actual:,.2f}")
