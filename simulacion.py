import time
import random
import os

class ruteadorA:

	def __init__(self):

		self.llamadasA = 0
		self.llamadaDesviada = 0
		self.llamadasRuteadasA = 0
		self.colaA = []
		self.ocupadoA = False

	def generarTiempoServicio(self):
		
		return 0

	def generarTiempoDesvio(self):
		
		return 0

	def generarTiempoArribo(self):
		
		return 0
                
	def generarEstadisticas(self):
		
		return 0

	def atenderLlamada(self, reloj, llamada, tiempoMax):

		reloj += eventos["E1"]
		llamada.generarTipoLlamada()
		llamada.setEntradaSistema(reloj)

		if self.ocupadoA == False:

			self.ocupadoA = True
			tiempoServicio = self.generarTiempoServicio()
			eventos["E4"] = reloj + tiempoServicio
			self.llamadasA += 1

		else:

			if len(self.colaA) == 5:

				tiempoDesvio = self.generarTiempoDesvio()
				eventos["E3"] = reloj + tiempoDesvio
				self.llamadaDesviada += 1

			else:

				self.colaA.append(llamada)
				llamada.setEntradaCola(reloj)

		tiempoArribo = self.generarTiempoArribo()
		eventos["E1"] = reloj + tiempoArribo

		if reloj >= tiempoMax:
			
			self.generarEstadisticas()
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo
			return False, reloj


class ruteadorB:

	def __init__(self):

		self.llamadasB = 0
		self.llamadasRuteadasB = 0
		self.llamadasPerdidas = 0
		self.colaB = []
		self.ocupadoB = False

	def generarTiempoServicio(self):

		return 0

	def generarTiempoServicioTipoUno(self):

		return 0

	def generarTiempoDesvio(self):

		return 0

	def generarTiempoArribo(self):

		return 0

	def generarEstadisticas(self):
		
		return 0

	def atenderLlamada(self, reloj, llamada, tiempoMax):

		reloj += eventos["E2"]

		if self.ocupadoB == False:

			self.ocupadoB = True
			tiempoServicio = self.generarTiempoServicio()
			eventos["E5"] = reloj + tiempoServicio
			self.llamadasB += 1

		else:

			if len(self.colaB) > 4:

				self.colaB.append(llamada)
				perdida = random.randint(0, 99)

				if perdida <= 10:

					self.colaB.pop()
					self.llamadasPerdidas += 1

			else:

				self.colaB.append(llamada)

		tiempoArribo = self.generarTiempoArribo()
		eventos["E2"] = reloj + tiempoArribo

		if reloj >= tiempoMax:
			
			self.generarEstadisticas()
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo
			return False, reloj

	def atenderLlamadaDesviada(self, reloj, llamada, tiempoMax):

		reloj += eventos["E3"]

		if self.ocupadoB == False:

			self.ocupadoB = True

			if llamada.tipoLlamada == 1:
			
				tiempoServicio = self.generarTiempoServicioTipoUno()
				eventos["E5"] = reloj + tiempoServicio

			else:
			
				tiempoServicio = self.generarTiempoServicio()
				eventos["E5"] = reloj + tiempoServicio

			self.llamadasB += 1

		else:

			if llamada.tipoLlamada == 2:

				if len(self.colaB) > 4:

					self.colaB.append(llamada)
					perdida = random.randint(0, 99)

					if perdida <= 10:

						self.colaB.pop()
						self.llamadasPerdidas += 1

				else:

					self.colaB.append(llamada)

			else:

				self.colaB.append(llamada)

		tiempoArribo = 0.5
		eventos["E2"] = reloj + tiempoArribo

		if reloj >= tiempoMax:
			
			self.generarEstadisticas()
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo
			return False, reloj

        
class llamada:
	
	def __init__(self):
		
		self.entradaSistema = 0
		self.salidaSistema = 0
		self.entradaCola = 0
		self.salidaCola = 0
		self.tipoLlamada = 0
		
	def generarTipoLlamada(self):
		
		tipo = random.randint(0, 99)
		
		if tipo >= 20:
			
			self.tipoLlamada = 1
			
		else:
			
			self.tipoLlamada = 2
			
	def obtenerTiempoEnCola(self):
		
		return self.salidaCola - self.entradaCola
		
	def obtenerTiempoEnSistema(self):
		
		return self.salidaSistema - self.entradaSistema
		
	def setEntradaSistema(self, entrada):
		
		self.entradaSistema = entrada
		
	def setSalidaSistema(self, salida):
		
		self.salidaSistema = salida
		
	def setEntradaCola(self, entrada):
		
		self.entradaCola = entrada
		
	def setSalidaCola(self, salida):
		
		self.salidaCola = salida
		

eventos = {
    "E1": 0,
    "E2": 0,
    "E3": 1000000000,
    "E4": 1000000000,
    "E5": 1000000000
}

def obtenerEventoMinimo():
		
	minimo = 1000000
	llave = ""

	for key in eventos:
		
		if eventos[key] < minimo:
			
			minimo = eventos[key]
			llave = key
			
	return llave

def main():
	
	os.system('cls' if os.name == 'nt' else 'clear')
	
	print("------------------------------")
	numeroCorridas = int(input("Ingrese la cantidad de corridas de la simulacion: "))
	maximoSimulacion = int(input("Ingrese el tiempo maximo para correr la simulacion (segundos): "))
	delay = input("¿Desea ver la simulacion correr en modo lento? (si/no): ")
	print("------------------------------")

	while numeroCorridas > 0:

		ruteA = ruteadorA()
		ruteB = ruteadorB()
		reloj = 0
		terminaSimulacion = False

		while True:

			evento = obtenerEventoMinimo()

			if evento == "E1":

				llamadaObj = llamada()
				terminaSimulacion, reloj = ruteA.atenderLlamada(reloj,  llamadaObj, maximoSimulacion)

			if evento == "E2":

				llamadaObj = llamada()
				terminaSimulacion, reloj = ruteB.atenderLlamada(reloj,  llamadaObj, maximoSimulacion)

			if terminaSimulacion:

				break

			if delay == "si":
				
				time.sleep(4)

		numeroCorridas -= 1

main()
