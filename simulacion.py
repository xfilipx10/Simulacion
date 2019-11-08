import time
import random
import os

class ruteadorA:

	def __init__(self):

		self.llamadasA = 0							# contador para las llamadas que entran a A
		self.llamadaDesviada = 0					# contador para las llamadas que se van a desviar
		self.llamadasRuteadasA = 0					# contador para las llamadas que A logre rutear
		self.colaA = []								# cola de llamadas en A
		self.llamadaPorSalir = []					# cola de llamada que van a salir del ruteador
		self.tiempoLlamadasSistema = []				# lista que va a tener el timepo en el sistema de cada llamada
		self.tiempoLlamadasCola = []				# lista que va a tener el tiempo en cola de cada llamada
		self.ocupadoA = False						# estado del ruteador

	# hay que programar todos los calculos de los tiempos y estadísticas

	def generarTiempoServicioTipoUno(self):
		
		return 2									# pruebas

	def generarTiempoServicioTipoDos(self):
		
		return 2									# pruebas

	def generarTiempoDesvio(self):
		
		return 1/2									# pruebas

	def generarTiempoArribo(self):
		
		return 0.001									# pruebas
                
	def generarEstadisticas(self):
		
		i = 1

		for tiempo in self.tiempoLlamadasSistema:

			print ("Tiempo en sistema llamada " + str(i) + " = " + str(tiempo))
			i += 1

		i = 1 
		print ("------------------------------")

		for tiempo in self.tiempoLlamadasCola:

			print ("Tiempo en cola llamada " + str(i) + " = " + str(tiempo))
			i += 1

		print ("------------------------------")
		return 0

	def imprimirRuteadorA(self):

		print ("Llamadas recibidas en A: " + str(self.llamadasA))
		print ("Llamadas ruteadas en A: " + str(self.llamadasRuteadasA))
		print ("Llamadas enviadas de A a B: " + str(self.llamadaDesviada))
		print ("Hay " + str(len(self.colaA)) + " llamadas en la cola A")
		print ("------------------------------")

	def atenderLlamada(self, reloj, llamada, tiempoMax):

		reloj += eventos["E1"]
		llamada.generarTipoLlamada()
		llamada.setEntradaSistema(reloj)
		self.llamadasA += 1

		if self.ocupadoA == False:

			self.ocupadoA = True

			if llamada.tipoLlamada == 1:
				tiempoServicio = self.generarTiempoServicioTipoUno()
			else:
				tiempoServicio = self.generarTiempoServicioTipoDos()
			
			eventos["E4"] = reloj + tiempoServicio
			self.llamadaPorSalir.append(llamada)

		else:

			if len(self.colaA) == 5:

				tiempoDesvio = self.generarTiempoDesvio()

				tiempos = eventos["E3"]
				tiempos.append(reloj + tiempoDesvio)

				self.llamadaDesviada += 1

			else:

				self.colaA.append(llamada)
				llamada.setEntradaCola(reloj)

		tiempoArribo = self.generarTiempoArribo()
		eventos["E1"] = reloj + tiempoArribo

		if reloj >= tiempoMax:
			
			# genera estadisticas
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo
			return False, reloj

	def salidaLlamada(self, reloj, tiempoMax):

		# actualiza el reloj con el tiempo que se programó para este evento
		# se programa el evento en infinito

		reloj += eventos["E4"]
		self.llamadasRuteadasA += 1

		# se saca la llamada que se le asignó a este evento
		# luego se establece el tiempo cuando sale del sistema
		# se coloca el tiempo en nuestra lista de tiempos
		# lo mismo para el tiempo en cola

		llamada = self.llamadaPorSalir.pop(0)

		llamada.setSalidaSistema(reloj)
		tiempoLlamadaSistema = llamada.obtenerTiempoEnSistema()
		self.tiempoLlamadasSistema.append(tiempoLlamadaSistema)

		tiempoLlamadaCola = llamada.obtenerTiempoEnCola()
		self.tiempoLlamadasCola.append(tiempoLlamadaCola)

		# esta parte me tiene confundido porque la profe había dicho que hay que revisar la cola
		# y si hay algo hay que atenderlo, pero no sé si eso significaba hacer el tiempo de atencion aqui
		# o llamar al evento de atender llamada

		if len(self.colaA) > 0:

			llamada = self.colaA.pop(0)
			llamada.setSalidaCola(reloj)
			self.llamadaPorSalir.append(llamada)

			if llamada.tipoLlamada == 1:
				tiempoServicio = self.generarTiempoServicioTipoUno()
			else:
				tiempoServicio = self.generarTiempoServicioTipoDos()

			eventos["E4"] = reloj + tiempoServicio

		else:

			self.ocupadoA = False
			eventos["E4"] = 100000000


		if reloj >= tiempoMax:
			
			# genera estadisticas
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo
			return False, reloj

class ruteadorB:

	def __init__(self):

		self.llamadasB = 0							# contador de llamadas totales que han llegado
		self.llamadasRuteadasB = 0					# contador de llamadas ruteadas
		self.llamadasPerdidas = 0					# contador de llamadas perdidas
		self.colaB = []								# cola de llamadas esperando a ser atendidas
		self.llamadaPorSalir = []					# cola de llamadas para salir del ruteador
		self.tiempoLlamadasSistema = []				# lista que va a tener el timepo en el sistema de cada llamada
		self.tiempoLlamadasCola = []				# lista que va a tener el tiempo en cola de cada llamada
		self.ocupadoB = False						# estado del ruteador

	# hay que programar todos los calculos de los tiempos y estadísticas

	def generarTiempoServicioTipoUno(self):

		return 2										# pruebas

	def generarTiempoServicioTipoDos(self):

		return 2									# pruebas

	def generarTiempoArribo(self):

		return 0.001										# pruebas

	def generarEstadisticas(self):
		
		i = 1

		for tiempo in self.tiempoLlamadasSistema:

			print ("Tiempo en sistema llamada " + str(i) + " = " + str(tiempo))
			i += 1

		i = 1 
		print ("------------------------------")

		for tiempo in self.tiempoLlamadasCola:

			print ("Tiempo en cola llamada " + str(i) + " = " + str(tiempo))
			i += 1

		print ("------------------------------")
		return 0

	def imprimirRuteadorB(self):

		print ("Llamadas recibidas en B: " + str(self.llamadasB))
		print ("Llamadas ruteadas en B: " + str(self.llamadasRuteadasB))
		print ("Llamadas perdidas en B: " + str(self.llamadasPerdidas))
		print ("------------------------------")

	def atenderLlamada(self, reloj, llamada, tiempoMax):

		reloj += eventos["E2"]
		
		llamada.setEntradaSistema(reloj)
		llamada.tipoLlamada = 2

		self.llamadasB += 1

		if self.ocupadoB == False:

			self.ocupadoB = True
			tiempoServicio = self.generarTiempoServicioTipoDos()
			eventos["E5"] = reloj + tiempoServicio
			self.llamadaPorSalir.append(llamada)

		else:

			if len(self.colaB) > 4:

				llamada.setEntradaCola(reloj)

				perdida = random.randint(0, 99)

				if perdida <= 10:

					self.llamadasPerdidas += 1
					llamada.mePerdi = True

				self.colaB.append(llamada)

			else:

				llamada.setEntradaCola(reloj)
				self.colaB.append(llamada)

		tiempoArribo = self.generarTiempoArribo()
		eventos["E2"] = reloj + tiempoArribo

		if reloj >= tiempoMax:
			
			# genera estadisticas
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo
			return False, reloj

	def atenderLlamadaDesviada(self, reloj, llamada, tiempoMax):

		tiempos = eventos["E3"]
		reloj += min(tiempos)

		for num in range(len(tiempos)):

			if tiempos[num] == min(tiempos):

				tiempos.pop(num)
				break

		llamada.setEntradaSistema(reloj)
		llamada.generarTipoLlamada()

		self.llamadasB += 1

		if self.ocupadoB == False:

			self.ocupadoB = True

			if llamada.tipoLlamada == 1:
			
				tiempoServicio = self.generarTiempoServicioTipoUno()
				eventos["E5"] = reloj + tiempoServicio
				self.llamadaPorSalir.append(llamada)

			else:
			
				tiempoServicio = self.generarTiempoServicioTipoDos()
				eventos["E5"] = reloj + tiempoServicio
				self.llamadaPorSalir.append(llamada)

		else:

			if llamada.tipoLlamada == 2:

				if len(self.colaB) > 4:

					llamada.setEntradaCola(reloj)

					perdida = random.randint(0, 99)

					if perdida <= 10:

						self.llamadasPerdidas += 1
						llamada.mePerdi = True

					self.colaB.append(llamada)

				else:

					llamada.setEntradaCola(reloj)
					self.colaB.append(llamada)

			else:

				llamada.setEntradaCola(reloj)
				self.colaB.append(llamada)

		if reloj >= tiempoMax:
			
			# genera estadisticas
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo
			return False, reloj

	def salidaLlamada(self, reloj, tiempoMax):

		# actualiza el reloj con el tiempo que se programó para este evento
		# se programa el evento en infinito

		reloj += eventos["E5"]
		self.llamadasRuteadasB += 1

		# se saca la llamada que se le asignó a este evento
		# luego se establece el tiempo cuando sale del sistema
		# se coloca el tiempo en nuestra lista de tiempos
		# lo mismo para el tiempo en cola

		llamada = self.llamadaPorSalir.pop(0)

		llamada.setSalidaSistema(reloj)
		tiempoLlamadaSistema = llamada.obtenerTiempoEnSistema()
		self.tiempoLlamadasSistema.append(tiempoLlamadaSistema)

		tiempoLlamadaCola = llamada.obtenerTiempoEnCola()

		if llamada.mePerdi == True:

			tiempoLlamadaCola += 0.5

		self.tiempoLlamadasCola.append(tiempoLlamadaCola)

		# esta parte me tiene confundido porque la profe había dicho que hay que revisar la cola
		# y si hay algo hay que atenderlo, pero no sé si eso significaba hacer el tiempo de atencion aqui
		# o llamar al evento de atender llamada

		if len(self.colaB) > 0:

			llamada = self.colaB.pop(0)
			llamada.setSalidaCola(reloj)
			self.llamadaPorSalir.append(llamada)

			if llamada.tipoLlamada == 1:
				tiempoServicio = self.generarTiempoServicioTipoUno()
			else:
				tiempoServicio = self.generarTiempoServicioTipoDos()

			eventos["E5"] = reloj + tiempoServicio

		else:

			self.ocupadoB = False
			eventos["E5"] = 100000000


		if reloj >= tiempoMax:
			
			# genera estadisticas
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
		self.mePerdi = False
		
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
		
# -----------------
# Hash para los eventos, aquí se establecen sus tiempos y se saca el mínimo para ver que evento sigue
# -----------------

eventos = {
    "E1": 0,
    "E2": 0,
    "E3": [1000000000],
    "E4": 1000000000,
    "E5": 1000000000
}

# -----------------
# Método para obtener el mínimo evento
# -----------------

def obtenerEventoMinimo():
		
	minimo = 1000000
	llave = ""

	for key in eventos:
		
		if key == "E3":

			data = eventos["E3"]
			
			if min(data) < minimo:

				minimo = min(data)
				llave = "E3"

		else:
		
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
		terminaCorrida = False

		while True:

			evento = obtenerEventoMinimo()

			if evento == "E1":

				llamadaObj = llamada()
				terminaCorrida, reloj = ruteA.atenderLlamada(reloj,  llamadaObj, maximoSimulacion)

			elif evento == "E2":

				llamadaObj = llamada()
				terminaCorrida, reloj = ruteB.atenderLlamada(reloj,  llamadaObj, maximoSimulacion)

			elif evento == "E3":

				llamadaObj = llamada()
				terminaCorrida, reloj = ruteB.atenderLlamadaDesviada(reloj, llamadaObj, maximoSimulacion)

			elif evento == "E4":

				terminaCorrida, reloj = ruteA.salidaLlamada(reloj, maximoSimulacion)

			elif evento == "E5":

				terminaCorrida, reloj = ruteB.salidaLlamada(reloj, maximoSimulacion)				

			if terminaCorrida:

				ruteA.generarEstadisticas()
				ruteB.generarEstadisticas()
				break

			if delay == "si":
				
				time.sleep(2)

			ruteA.imprimirRuteadorA()
			ruteB.imprimirRuteadorB()

		numeroCorridas -= 1

		eventos["E1"] = 0
		eventos["E2"] = 0
		eventos["E3"] = [1000000000]
		eventos["E4"] = 1000000000
		eventos["E5"] = 1000000000

main()
