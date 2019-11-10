import time
import random
import os
import math
import random

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
		self.acumuladorColaA = 0					# acumulador para las llamadas en cola que fueron ruteadas por A
		self.acumuladorTiempoSis = 0 				# acumulador para el tiempo promedio en el sistema

	def generarTiempoServicioTipoUno(self):
		
		return math.sqrt((500*random.random())+400)	

	def generarTiempoServicioTipoDos(self):
		
		x = 0

		while True:

			z = 0
			i = 0

			while i < 12:
			
				z += random.random()
				i += 1
		
			z -= 6
		
			x = 1 * z + 15

			if x > 0:
				break
		
		return x									

	def generarTiempoDesvio(self):
		
		return 1/2									

	def generarTiempoArribo(self):
		
		r = 0

		while True:

			r = random.random()
			if r != 1:
				break

		num = -math.log(1-r)
		den = 2/3
		
		return num/den

	def getLlamadasRuteadas(self):

		return self.llamadasRuteadasA
                
	def generarEstadisticas(self, totalRuteadaB):

		print ("Estadísticas de A")

		'''

		i = 1

		for tiempo in self.tiempoLlamadasSistema:

			print ("Tiempo en sistema llamada " + str(i) + " = " + str(tiempo))
			i += 1

		i = 1 

		print ("")

		for tiempo in self.tiempoLlamadasCola:

			print ("Tiempo en cola llamada " + str(i) + " = " + str(tiempo))
			i += 1

		'''

		tiempoSis = self.acumuladorTiempoSis / (self.llamadasRuteadasA + totalRuteadaB)
		print ("Tiempo promedio de permanencia de una llamada en el sistema: {:.2f}".format(tiempoSis))

		tiempoPromCola = self.acumuladorColaA / (self.llamadasRuteadasA + totalRuteadaB)
		print ("Tiempo promedio en cola de llamadas ruteadas por A: {:.2f}".format(tiempoPromCola))

		eficiencia = tiempoPromCola / tiempoSis
		print ("Eficiencia del sistema con las llamadas que llegaron a A: {:.2f}".format(eficiencia))

		print ("------------------------------")
		return 0

	def imprimirRuteadorA(self):

		if self.ocupadoA:
			print ("Estado ruteador A: ocupado")
		else:
			print ("Estado ruteador A: libre")

		print ("Llamadas recibidas en A: " + str(self.llamadasA))
		print ("Llamadas ruteadas en A: " + str(self.llamadasRuteadasA))
		print ("Llamadas enviadas de A a B: " + str(self.llamadaDesviada))
		print ("Llamadas en cola A: " + str(len(self.colaA)))
		print ("")

	def atenderLlamada(self, reloj, llamada, tiempoMax):

		reloj = eventos["E1"]
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

		reloj = eventos["E4"]
		self.llamadasRuteadasA += 1

		# se saca la llamada que se le asignó a este evento
		# luego se establece el tiempo cuando sale del sistema
		# se coloca el tiempo en nuestra lista de tiempos
		# lo mismo para el tiempo en cola

		llamada = self.llamadaPorSalir.pop(0)

		llamada.setSalidaSistema(reloj)
		tiempoLlamadaSistema = llamada.obtenerTiempoEnSistema()
		self.tiempoLlamadasSistema.append(tiempoLlamadaSistema)
		self.acumuladorTiempoSis += tiempoLlamadaSistema

		tiempoLlamadaCola = llamada.obtenerTiempoEnCola()
		self.tiempoLlamadasCola.append(tiempoLlamadaCola)
		self.acumuladorColaA += tiempoLlamadaCola

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
		self.acumuladorColaB = 0					# acumulador del tiempo en cola de las llamadas que llegaron directo a B
		self.acumuladorColaDesviadas = 0 			# acumulador del tiempo en cola de las llamadas desviadas
		self.acumuladorTiempoSis = 0				# acumulador del tiempo en permanencia en el sistema de las que llegaron directas
		self.acumuladorTiempoDes = 0				# acumulador del tiempo en permanencia en el sistema de las que llegaron desviadas
		self.acumuladorTamanoColaB = 0 				# acumulador para el tamaño de la colaB con respecto al tiempo
		self.ultimoCambioColaB = 0					# variable que va a tener el tiempo para el ultimo cambio que se hizo en la cola

	def generarTiempoServicioTipoUno(self):

		r = random.random()

		usarPrimeraFormula = 2*r
		if usarPrimeraFormula <= 1:

			return usarPrimeraFormula

		else:

			usarSegundaFormula = 3 - math.sqrt(8 - (8*r))
			return usarSegundaFormula										

	def generarTiempoServicioTipoDos(self):

		r = 0

		while True:

			r = random.random()
			if r != 1:
				break

		num = -math.log(1-r)
		den = 4/3
		
		return num/den										

	def generarTiempoArribo(self):

		return random.random()*(3-1)+1

	def getLlamadasRuteadas(self):

		return self.llamadasRuteadasB

	def actualizarUltimoValorCola(self, reloj):

		self.acumuladorTamanoColaB += len(self.colaB) * (reloj - self.ultimoCambioColaB)
		self.ultimoCambioColaB = reloj

	def generarEstadisticas(self, totalRuteadaA, reloj):
		
		print ("Estadísticas de B")

		'''

		i = 1

		for tiempo in self.tiempoLlamadasSistema:

			print ("Tiempo en sistema llamada " + str(i) + " = " + str(tiempo))
			i += 1

		i = 1

		print ("")

		for tiempo in self.tiempoLlamadasCola:

			print ("Tiempo en cola llamada " + str(i) + " = " + str(tiempo))
			i += 1

		'''

		tamPromCola = self.acumuladorTamanoColaB / reloj
		print ("Tamaño promedio de la cola en B: {:.2f}".format(tamPromCola))

		tiempoSis = self.acumuladorTiempoSis / (self.llamadasRuteadasB + totalRuteadaA)
		print ("Tiempo promedio de permanencia de las llamadas que llegaron a B: {:.2f}".format(tiempoSis))

		tiempoSisDes = self.acumuladorTiempoDes / (self.llamadasRuteadasB + totalRuteadaA)
		print ("Tiempo promedio de permanencia de las llamadas que llegaron de A a B: {:.2f}".format(tiempoSisDes))

		tiempoPromColaB = self.acumuladorColaB / (self.llamadasRuteadasB + totalRuteadaA)
		tiempoPromColaDes = self.acumuladorColaDesviadas / (self.llamadasRuteadasB + totalRuteadaA)

		print ("Tiempo promedio en cola de llamadas que llegaron a B: {:.2f}".format(tiempoPromColaB))
		print ("Tiempo promedio en cola de llamadas que llegaron desde A a B: {:.2f}".format(tiempoPromColaDes))

		eficienciaB = tiempoPromColaB / tiempoSis
		eficienciaAaB = tiempoPromColaDes / tiempoSisDes

		print ("Eficiencia del sistema con las llamadas que llegaron a B: {:.2f}".format(eficienciaB))
		print ("Eficiencia del sistema con las llamada que llegaron desde A a B: {:.2f}".format(eficienciaAaB))

		porcentajePerdidas = self.llamadasPerdidas*100 / (self.llamadasRuteadasB + totalRuteadaA)
		print ("Porcentaje de llamadas perdidas: {:.2f}%".format(porcentajePerdidas))

		print ("------------------------------")
		return 0

	def imprimirRuteadorB(self):

		if self.ocupadoB:
			print ("Estado ruteador B: ocupado")
		else:
			print ("Estado ruteador B: libre")

		print ("Llamadas recibidas en B: " + str(self.llamadasB))
		print ("Llamadas ruteadas en B: " + str(self.llamadasRuteadasB))
		print ("Llamadas perdidas en B: " + str(self.llamadasPerdidas))
		print ("Llamadas en cola B: " + str(len(self.colaB)))
		print ("")

	def atenderLlamada(self, reloj, llamada, tiempoMax):

		reloj = eventos["E2"]
		
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

				perdida = random.randint(0, 99)

				if perdida <= 10:

					self.llamadasPerdidas += 1
					llamada.mePerdi = True

			llamada.setEntradaCola(reloj)
			self.colaB.append(llamada)
			self.acumuladorTamanoColaB += len(self.colaB) * (reloj - self.ultimoCambioColaB)
			self.ultimoCambioColaB = reloj

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
		reloj = min(tiempos)

		for num in range(len(tiempos)):

			if tiempos[num] == min(tiempos):

				tiempos.pop(num)
				break

		llamada.setEntradaSistema(reloj)
		llamada.generarTipoLlamada()
		llamada.meDesviaron = True

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

			self.acumuladorTamanoColaB += len(self.colaB) * (reloj - self.ultimoCambioColaB)
			self.ultimoCambioColaB = reloj

		if reloj >= tiempoMax:
			
			# genera estadisticas
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo
			return False, reloj

	def salidaLlamada(self, reloj, tiempoMax):

		# actualiza el reloj con el tiempo que se programó para este evento
		# se programa el evento en infinito

		reloj = eventos["E5"]
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

		if llamada.meDesviaron == True:

			tiempoLlamadaCola += 0.5
			self.acumuladorColaDesviadas += tiempoLlamadaCola
			self.acumuladorTiempoDes += tiempoLlamadaSistema

		else:

			self.acumuladorColaB += tiempoLlamadaCola
			self.acumuladorTiempoSis += tiempoLlamadaSistema

		self.tiempoLlamadasCola.append(tiempoLlamadaCola)

		if len(self.colaB) > 0:

			llamada = self.colaB.pop(0)
			llamada.setSalidaCola(reloj)
			self.llamadaPorSalir.append(llamada)

			self.acumuladorTamanoColaB += len(self.colaB) * (reloj - self.ultimoCambioColaB)
			self.ultimoCambioColaB = reloj

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
		self.meDesviaron = False
		
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

				ruteA.generarEstadisticas(ruteB.getLlamadasRuteadas())
				ruteB.actualizarUltimoValorCola(reloj)
				ruteB.generarEstadisticas(ruteA.getLlamadasRuteadas(), reloj)

				break

			if delay == "si":
				
				time.sleep(2)

			print ("Reloj actual del sistema: {:.2f}".format(reloj))
			print ("Evento que se va a procesar: " + evento + "\n")

			ruteA.imprimirRuteadorA()
			ruteB.imprimirRuteadorB()

			print ("------------------------------")

		numeroCorridas -= 1

		eventos["E1"] = 0
		eventos["E2"] = 0
		eventos["E3"] = [1000000000]
		eventos["E4"] = 1000000000
		eventos["E5"] = 1000000000

main()
