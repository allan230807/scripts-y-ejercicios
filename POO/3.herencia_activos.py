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

class Accion(ActivoFinanciero):
    def __init__(self, ticker, precio_actual, dividendo_anual):
        super().__init__(ticker, precio_actual)
        self.dividendo_anual = dividendo_anual

    def calcular_dividend_yield(self):
        return self.dividendo_anual / self.precio_actual

class Cryptoactivo(ActivoFinanciero):
    def __init__(self, ticker, precio_actual, comision_red):
        super().__init__(ticker, precio_actual)
        self.comision = comision_red

    def registrar_rendimeinto(self, rendimiento):
        super().registrar_rendimiento(rendimiento)
        self.precio_actual *= 1 - self.comision_red

if __name__ == "__main__":
    apple = Accion("AAPL", 220.0, dividendo_anual=2.0)
    bitcoin = Cryptoactivo("BTC", 65000.0, comision_red=0.001)

    apple.simulacion_rendimientos(30, 0.001, 0.015)
    bitcoin.simulacion_rendimientos(30, 0.002, 0.04)

    print(apple)
    print(
        f"Dividend Yield de Apple: {apple.calcular_dividend_yield() * 100:.2f}%\n"
    )

    print(bitcoin)




    

    


