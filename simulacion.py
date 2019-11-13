import time
import random
import os
import math
import random

class ruteadorA:

	def __init__(self):

		self.llamadasA = 0							# contador para las llamadas que entran a A
		self.llamadaDesviada = 0					# contador para las llamadas que se van a desviar
		self.llamadasRuteadasA = 0					# contador para las llamadas que A logre rutear en total
		self.colaA = []								# cola de llamadas en A
		self.llamadaPorSalir = []					# cola de llamada que van a salir del ruteador
		self.ocupadoA = False						# estado del ruteador
		self.acumuladorColaA = 0					# acumulador para las llamadas en cola que fueron ruteadas por A
		self.acumuladorTiempoSis = 0 				# acumulador para el tiempo promedio en el sistema
		self.llamadasRuteadasLocales = 0			# contador para las llamadas locales que procese A
		self.llamadasRuteadasLarga = 0				# contador para las llamadas larga distancia que procese A

	# generador para el tiempo de servicio para llamadas de larga distancia
	def generarTiempoServicioTipoUno(self):
		
		return math.sqrt((500*random.random())+400)	

	# generador para el tiempo de servicio para llamadas locales
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

	# tiempo constante de desvío hacia B
	def generarTiempoDesvio(self):
		
		return 1/2									

	# generador del tiempo de arribo para A
	def generarTiempoArribo(self):
		
		r = 0

		while True:

			r = random.random()
			if r != 1:
				break

		num = -math.log(1-r)
		den = 2/3
		
		return num/den

	# método get que devuelve el total de llamadas ruteadas por A
	def getLlamadasRuteadas(self):

		return self.llamadasRuteadasA

	# método get para llamadas locales, este método lo usa B para el porcentaje de llamadas perdidas   
	def getLlamadasLocales(self):

		return self.llamadasRuteadasLocales
	
	# método que genera las estadísticas de A al final de una corrida
	def generarEstadisticas(self):

		print ("Estadísticas de A")

		# revisa si A ha ruteado llamadas para no dividir por cero
		if self.llamadasRuteadasA > 0:

			tiempoSis = self.acumuladorTiempoSis / (self.llamadasRuteadasA)
			print ("Tiempo promedio de permanencia de una llamada en el sistema: {:.2f}".format(tiempoSis))

			tiempoPromCola = self.acumuladorColaA / (self.llamadasRuteadasA)
			print ("Tiempo promedio en cola de llamadas ruteadas por A: {:.2f}".format(tiempoPromCola))

			eficiencia = tiempoPromCola / tiempoSis
			print ("Eficiencia del sistema con las llamadas que llegaron a A: {:.2f}".format(eficiencia))

			print ("------------------------------")
			return [tiempoSis, tiempoPromCola, eficiencia]
		
		# si no ha ruteadoo, despliega el mensaje, y devuelve un array de ceros para las estadísticas
		print ("El ruteador A no ha ruteado ninguna llamada a la hora de terminar la simulación.")
		print ("------------------------------")
		return [0,0,0]

	# método que imprime los contadores de A que se despliegan por evento
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

	# método para el evento de entrada de llamada al ruteador A
	def atenderLlamada(self, reloj, llamada, tiempoMax):

		# actualiza reloj, genera tipo de llamada, establece entrada al sistema y le suma al contador del total de llamadas que ha recibido A
		reloj = eventos["E1"]
		llamada.generarTipoLlamada()
		llamada.setEntradaSistema(reloj)
		self.llamadasA += 1

		# si el ruteador está libre, lo pone en ocupado, genera tiempo de servicio respectivo al tipo de llamada y programa evento E4
		if self.ocupadoA == False:

			self.ocupadoA = True

			if llamada.tipoLlamada == 1:
				tiempoServicio = self.generarTiempoServicioTipoUno()
			else:
				tiempoServicio = self.generarTiempoServicioTipoDos()
			
			eventos["E4"] = reloj + tiempoServicio
			self.llamadaPorSalir.append(llamada)

		else:

			# si el ruteador está ocupado, revisa si la cola es igual a 5, si sí, entonces genera tiempo de desvío, programa evento E3, y le suma al contador de desviadas
			# y agrega ese evento a la cola de eventos para llamadas desviada, con el fin de no caerle encima a una que ya estaba programada
			if len(self.colaA) == 5:

				tiempoDesvio = self.generarTiempoDesvio()

				tiempos = eventos["E3"]
				tiempos.append(reloj + tiempoDesvio)
				
				colaDesviadas.append(llamada)

				self.llamadaDesviada += 1

			else:

				# si la cola no era igual a cinco, simplemente establece el tiempo de entrada a cola, y mete la llamada a cola
				self.colaA.append(llamada)
				llamada.setEntradaCola(reloj)

		# genera tiempo de arribo y programa el siguiente evento E1
		tiempoArribo = self.generarTiempoArribo()
		eventos["E1"] = reloj + tiempoArribo

		if reloj >= tiempoMax:
			
			# genera estadisticas, siempre devuelve reloj, para que el siguiente evento tenga el reloj actualizado
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo, siempre devuelve reloj, para que el siguiente evento tenga el reloj actualizado
			return False, reloj

	# método para el evento salida de llamada del ruteador A
	def salidaLlamada(self, reloj, tiempoMax):

		# actualiza reloj, suma a la variable de llamadas ruteadas por A, saca la llamada de la cola por salir
		reloj = eventos["E4"]
		self.llamadasRuteadasA += 1

		llamada = self.llamadaPorSalir.pop(0)

		# dependiendo del tipo de llamada le suma al contador respectivo
		if llamada.tipoLlamada == 1:

			self.llamadasRuteadasLarga += 1

		else:

			self.llamadasRuteadasLocales += 1

		# establece tiempo de salida del sistema y lo acumula, e igualmente con el tiempo de cola
		llamada.setSalidaSistema(reloj)
		tiempoLlamadaSistema = llamada.obtenerTiempoEnSistema()
		self.acumuladorTiempoSis += tiempoLlamadaSistema

		tiempoLlamadaCola = llamada.obtenerTiempoEnCola()
		self.acumuladorColaA += tiempoLlamadaCola

		# si la longitud de la cola es mayor a cero, saca llamada de cola, le establece el tiempo de salida en cola, y agrega a cola de llamadas por salir
		if len(self.colaA) > 0:

			llamada = self.colaA.pop(0)
			llamada.setSalidaCola(reloj)
			self.llamadaPorSalir.append(llamada)

			# dependiendo del tipo de llamada genera su tiempo de servicio y programa evento E4 (salida de llamada del ruteador A)
			if llamada.tipoLlamada == 1:
				tiempoServicio = self.generarTiempoServicioTipoUno()
			else:
				tiempoServicio = self.generarTiempoServicioTipoDos()

			eventos["E4"] = reloj + tiempoServicio

		else:

			# si no hay nadie en cola, pone que el ruteador está libre y desprograma el evento
			self.ocupadoA = False
			eventos["E4"] = 100000000


		if reloj >= tiempoMax:
			
			# genera estadisticas, siempre devuelve reloj, para que el siguiente evento tenga el reloj actualizado
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo, siempre devuelve reloj, para que el siguiente evento tenga el reloj actualizado
			return False, reloj

class ruteadorB:

	def __init__(self):

		self.llamadasB = 0							# contador de llamadas totales que han llegado
		self.llamadasRuteadasB = 0					# contador de llamadas ruteadas
		self.llamadasPerdidas = 0					# contador de llamadas perdidas
		self.colaB = []								# cola de llamadas esperando a ser atendidas
		self.llamadaPorSalir = []					# cola de llamadas para salir del ruteador
		self.ocupadoB = False						# estado del ruteador
		self.acumuladorColaB = 0					# acumulador del tiempo en cola de las llamadas que llegaron directo a B
		self.acumuladorColaDesviadas = 0 			# acumulador del tiempo en cola de las llamadas desviadas
		self.acumuladorTiempoSis = 0				# acumulador del tiempo en permanencia en el sistema de las que llegaron directas
		self.acumuladorTiempoDes = 0				# acumulador del tiempo en permanencia en el sistema de las que llegaron desviadas
		self.acumuladorTamanoColaB = 0 				# acumulador para el tamaño de la colaB con respecto al tiempo
		self.ultimoCambioColaB = 0					# variable que va a tener el tiempo para el ultimo cambio que se hizo en la cola
		self.llamadasRuteadasDirectas = 0			# contador para las llamadas directas que rutea B
		self.llamadasRuteadasLocales = 0			# contador llamadas locales
		self.llamadasRuteadasDesviadas = 0			# contador para llamadas ruteadas desviadas

	# generador para el tiempo de servicio de las llamadas larga distancia
	def generarTiempoServicioTipoUno(self):

		r = random.random()

		usarPrimeraFormula = 2*r
		if usarPrimeraFormula <= 1:

			return usarPrimeraFormula

		else:

			usarSegundaFormula = 3 - math.sqrt(8 - (8*r))
			return usarSegundaFormula										

	# generador para el tiempo de servicio de las llamadas locales
	def generarTiempoServicioTipoDos(self):

		r = 0

		while True:

			r = random.random()
			if r != 1:
				break

		num = -math.log(1-r)
		den = 4/3
		
		return num/den										

	# generador del tiempo de arribo a B
	def generarTiempoArribo(self):

		return random.random()*(3-1)+1

	# método get para las llamadas ruteadas por B
	def getLlamadasRuteadas(self):

		return self.llamadasRuteadasB

	# método que se utiliza al final de una corrida, para actualizar el acumulador del tamaño promedio de la cola B, con el ultimo valor que tuvo el reloj
	def actualizarUltimoValorCola(self, reloj):

		self.acumuladorTamanoColaB += len(self.colaB) * (reloj - self.ultimoCambioColaB)
		self.ultimoCambioColaB = reloj

	# método que genera las estadísticas de B al final de una corrida
	def generarEstadisticas(self, llamadaLocalA,reloj):
		
		print ("Estadísticas de B")

		tamPromCola = 0
		tiempoSis = 0
		tiempoSisDes = 0
		tiempoPromColaB = 0
		tiempoPromColaDes = 0
		eficienciaB = 0
		eficienciaAaB = 0
		porcentajePerdidas = 0

		# revisa si se ha ruteado aunque sea una llamada, ya sea directa o desviada, para no hacer divisiones entre cero
		if self.llamadasRuteadasB > 0:

			# imprime el tamaño promedio de cola, utilizando el reloj en el cual terminó la corrida, el cual puede ser mayor al max de la simulación
			tamPromCola = self.acumuladorTamanoColaB / reloj
			print ("Tamaño promedio de la cola en B: {:.2f}".format(tamPromCola))

			# revisa si el ruteador ruteó llamadas directas, para no hacer divisiones entre cero
			if self.llamadasRuteadasDirectas > 0:

				tiempoSis = self.acumuladorTiempoSis / (self.llamadasRuteadasDirectas)
				print ("Tiempo promedio de permanencia de las llamadas que llegaron a B: {:.2f}".format(tiempoSis))

				tiempoPromColaB = self.acumuladorColaB / (self.llamadasRuteadasDirectas)
				print ("Tiempo promedio en cola de llamadas que llegaron a B: {:.2f}".format(tiempoPromColaB))

				eficienciaB = tiempoPromColaB / tiempoSis
				print ("Eficiencia del sistema con las llamadas que llegaron a B: {:.2f}".format(eficienciaB))

			else:

				print ("El ruteador B no ha ruteado ninguna llamada directa a la hora de terminar la simulación.")

			# revisa si el ruteador ruteó llamadas directas, para no hacer divisiones entre cero
			if self.llamadasRuteadasDesviadas > 0:

				tiempoSisDes = self.acumuladorTiempoDes / (self.llamadasRuteadasDesviadas)
				print ("Tiempo promedio de permanencia de las llamadas que llegaron de A a B: {:.2f}".format(tiempoSisDes))

				tiempoPromColaDes = self.acumuladorColaDesviadas / (self.llamadasRuteadasDesviadas)
				print ("Tiempo promedio en cola de llamadas que llegaron desde A a B: {:.2f}".format(tiempoPromColaDes))

				eficienciaAaB = tiempoPromColaDes / tiempoSisDes
				print ("Eficiencia del sistema con las llamada que llegaron desde A a B: {:.2f}".format(eficienciaAaB))

			else:

				print ("El ruteador B no ha ruteado ninguna llamada desviada a la hora de terminar la simulación.")

			porcentajePerdidas = self.llamadasPerdidas*100 / (self.llamadasRuteadasLocales + llamadaLocalA)
			print ("Porcentaje de llamadas perdidas: {:.2f}%".format(porcentajePerdidas))

			print ("------------------------------")
			return [tamPromCola, tiempoSis, tiempoSisDes, tiempoPromColaB, tiempoPromColaDes, eficienciaB, eficienciaAaB, porcentajePerdidas]

		# si no ha ruteado nada, simplemente imprime lo siguiente, y devuelve un array de estadísticas en cero
		print ("El ruteador B no ha ruteado ninguna llamada a la hora de terminar la simulación.")
		print ("------------------------------")
		return [0,0,0,0,0,0,0,0]

	# método que imprime los contadores de B que se despliegan por evento
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

	# método que atiende llamadas que entran directo a B
	def atenderLlamada(self, reloj, llamada, tiempoMax):

		# se actualiza reloj, se establece tiempo de entrada al sistema, y ya que es llamada directa a B se pone su tipo de llamada en local
		reloj = eventos["E2"]
		
		llamada.setEntradaSistema(reloj)
		llamada.tipoLlamada = 2

		self.llamadasB += 1

		# si el ruteador está libre, se genera su tiemp de servicio y se programa el evento E5	
		if self.ocupadoB == False:

			self.ocupadoB = True
			tiempoServicio = self.generarTiempoServicioTipoDos()
			eventos["E5"] = reloj + tiempoServicio
			self.llamadaPorSalir.append(llamada)

		else:

			# si está ocupado, se pone su tiempo en cola a la llamada
			# ya que hubo cambio en la cola, se actualiza el acumulador del tamaño promedio de la cola B con respecto al tiempo
			llamada.setEntradaCola(reloj)
			self.colaB.append(llamada)
			self.acumuladorTamanoColaB += len(self.colaB) * (reloj - self.ultimoCambioColaB)
			self.ultimoCambioColaB = reloj

		# se genera tiempo de arribo para la siguiente llamada y se programa el evento E2
		tiempoArribo = self.generarTiempoArribo()
		eventos["E2"] = reloj + tiempoArribo

		if reloj >= tiempoMax:
			
			# genera estadisticas, siempre devuelve reloj, para que el siguiente evento tenga el reloj actualizado
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo, siempre devuelve reloj, para que el siguiente evento tenga el reloj actualizado
			return False, reloj

	# método que atiende llamadas desviadas que llegaron de A
	def atenderLlamadaDesviada(self, reloj, llamada, tiempoMax):

		# se actualiza el reloj con el evento mínimo de las llamadas desviadas
		tiempos = eventos["E3"]
		reloj = min(tiempos)

		# ya que las llamadas desviadas pueden ser varias, se revisa cual es la minima para sacarla de esa cola de llamadas desviadas
		for num in range(len(tiempos)):

			if tiempos[num] == min(tiempos):

				tiempos.pop(num)
				break

		# se saca la llamada de cola desviada, se establece su variable de desviada en true
		llamada = colaDesviadas.pop(0)
		llamada.meDesviaron = True

		self.llamadasB += 1

		# si el ruteador no esta ocupado, se procesa la llamada, dependiendo de su tipo se genera el tiempo de servicio respectivo y se programa el evento E5
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

			# si el ruteador está ocupado, se establece el tiempo de entrada cola
			# ya que hubo cambio en la cola, se actualiza el acumulador del tamaño promedio de la cola con respecto al tiempo de cambio
			llamada.setEntradaCola(reloj)
			self.colaB.append(llamada)

			self.acumuladorTamanoColaB += len(self.colaB) * (reloj - self.ultimoCambioColaB)
			self.ultimoCambioColaB = reloj

		if reloj >= tiempoMax:
			
			# genera estadisticas, siempre devuelve reloj, para que el siguiente evento tenga el reloj actualizado
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo, siempre devuelve reloj, para que el siguiente evento tenga el reloj actualizado
			return False, reloj

	# método para el evento E5 el cual es la salida de llamda del ruteador B
	def salidaLlamada(self, reloj, tiempoMax):

		# se actualiza reloj, contador de llamadas totales ruteadas, se saca la llamada que se va a atender, se establece su tiempo de salida del sistema
		# se suma a los acumuladores de tiempo en el sistema, y tiempo en cola sus respectivos tiempos de la llamada
		reloj = eventos["E5"]
		self.llamadasRuteadasB += 1

		llamada = self.llamadaPorSalir.pop(0)
		llamada.setSalidaSistema(reloj)

		tiempoLlamadaSistema = llamada.obtenerTiempoEnSistema()
		tiempoLlamadaCola = llamada.obtenerTiempoEnCola()

		# si la llamada fue desviada, se actualizan sus respectivos contadores y sus respectivos tiempos
		if llamada.meDesviaron == True:

			tiempoLlamadaCola += 0.5
			self.acumuladorColaDesviadas += tiempoLlamadaCola
			self.acumuladorTiempoDes += tiempoLlamadaSistema
			self.llamadasRuteadasDesviadas += 1

			# si es local, se actualiza contador de llamadas locales ruteadas por B
			if llamada.tipoLlamada == 2:

				self.llamadasRuteadasLocales += 1

		else:

			# si no fue desviada, entonces se actualizan sus respectivos contadores y tiempos
			self.llamadasRuteadasLocales += 1
			self.llamadasRuteadasDirectas += 1
			self.acumuladorColaB += tiempoLlamadaCola
			self.acumuladorTiempoSis += tiempoLlamadaSistema

		# una vez que fue atendida, se procede a revisar si la llamada es local y el estado de la cola, si las condiciones se dan se genera la proba de perdida
		if llamada.tipoLlamada == 2:

			if len(self.colaB) > 4:

					perdida = random.randint(0, 99)

					if perdida < 10:

						llamada.mePerdi = True
						self.llamadasPerdidas += 1

		if len(self.colaB) > 0:

			# si hay llamada en cola, saca a la primera que se ingresó, le establece su tiempo de salida de cola y la pone en la cola de llamadas por salir
			# ya que hubo cambio en la colaB, se actualiza ese cambio en el acumulador con su respectivo tiempo, luego se actualiza el tiempo del ultimo cambio
			llamada = self.colaB.pop(0)
			llamada.setSalidaCola(reloj)
			self.llamadaPorSalir.append(llamada)

			self.acumuladorTamanoColaB += len(self.colaB) * (reloj - self.ultimoCambioColaB)
			self.ultimoCambioColaB = reloj

			# dependiendo del tipo de llamada, se genera un tiempo de servicio, y se programa el evento E5 (salida de llamada en ruteadorB)
			if llamada.tipoLlamada == 1:
				tiempoServicio = self.generarTiempoServicioTipoUno()
			else:
				tiempoServicio = self.generarTiempoServicioTipoDos()

			eventos["E5"] = reloj + tiempoServicio

		else:

			# si cola no está llena, pone ruteador en desocupado y desprograma evento
			self.ocupadoB = False
			eventos["E5"] = 100000000


		if reloj >= tiempoMax:
			
			# genera estadisticas, siempre devuelve reloj, para que el siguiente evento tenga el reloj actualizado
			return True, reloj
						
		else: 
			
			# buscar siguiente minimo, siempre devuelve reloj, para que el siguiente evento tenga el reloj actualizado
			return False, reloj

        
class llamada:
	
	def __init__(self):
		
		self.entradaSistema = 0				# variable que almacena el tiempo de entrada al sistema de una llamada
		self.salidaSistema = 0				# variable que almacena el tiempo de salida del sistema de una llamada
		self.entradaCola = 0				# variable que almacena el tiempo de entrada a cola de una llamada
		self.salidaCola = 0					# variable que almacena el tiempo de salida de cola de una llamada
		self.tipoLlamada = 0				# variable que almacena el tipo de llamada (larga o local)
		self.mePerdi = False				# booleano que representa si la llamada se pierde o no
		self.meDesviaron = False			# booleano que representa si la llamada es desviada o no
		
	# método que genera un tipo de llamada, 20% de que sea larga distancia, 80% de que sea local
	def generarTipoLlamada(self):
		
		tipo = random.randint(0, 99)
		
		if tipo < 20:
			
			self.tipoLlamada = 1
			
		else:
			
			self.tipoLlamada = 2
			
	# método get tiempo en cola
	def obtenerTiempoEnCola(self):
		
		return self.salidaCola - self.entradaCola
		
	# método get tiempo en el sistema
	def obtenerTiempoEnSistema(self):
		
		return self.salidaSistema - self.entradaSistema
		
	# método set tiempo de entrada al sistema
	def setEntradaSistema(self, entrada):
		
		self.entradaSistema = entrada

	# método set tiempo de salida del sistema	
	def setSalidaSistema(self, salida):
		
		self.salidaSistema = salida
		
	# método set tiempo de entrada a cola
	def setEntradaCola(self, entrada):
		
		self.entradaCola = entrada
		
	# método set tiempo de salida de cola
	def setSalidaCola(self, salida):
		
		self.salidaCola = salida
		
# -----------------
# Hash para los eventos, aquí se establecen sus tiempos y se saca el mínimo para ver que evento sigue
# El evento E3 es una lista, ya que se puede dar el caso de que haya varias llamadas en cola
# -----------------

eventos = {
    "E1": 0,
    "E2": 0,
    "E3": [1000000000],
    "E4": 1000000000,
    "E5": 1000000000
}

# -----------------
# Cola para llamadas desviadas, acumuladores para promedios finales al final de la simulación
# -----------------

colaDesviadas = []
tamPromColaB = 0
tiempoSisB = 0
tiempoSisDes = 0
tiempoPromColaB = 0
tiempoPromColaDes = 0
eficienciaB = 0
eficienciaAaB = 0
porcentajePerdidas = 0
tiempoSisA = 0
tiempoPromColaA = 0
eficienciaA = 0

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

# -----------------
# Método para almacenar el promedio del promedio de las estadísticas
# -----------------

def promedioDepromedios(array, ruteador):

	global tamPromColaB
	global tiempoSisB
	global tiempoSisDes
	global tiempoPromColaB
	global tiempoPromColaDes
	global eficienciaB
	global eficienciaAaB
	global porcentajePerdidas
	global tiempoSisA
	global tiempoPromColaA
	global eficienciaA

	if ruteador == "B":

		tamPromColaB += array[0]
		tiempoSisB += array[1]
		tiempoSisDes += array[2]
		tiempoPromColaB += array[3]
		tiempoPromColaDes += array[4]
		eficienciaB += array[5]
		eficienciaAaB += array[6]
		porcentajePerdidas += array[7]

	else:

		tiempoSisA += array[0]
		tiempoPromColaA += array[1]
		eficienciaA += array[2]

# -----------------
# Método para desplegar el promedio del promedio de las estadísticas
# -----------------

def imprimirPromedios(corridas):

	print ("Estadísticas de A")
	print ("Tiempo promedio de permanencia de una llamada en el sistema: {:.2f}".format(tiempoSisA/corridas))
	print ("Tiempo promedio en cola de llamadas ruteadas por A: {:.2f}".format(tiempoPromColaA/corridas))
	print ("Eficiencia del sistema con las llamadas que llegaron a A: {:.2f}\n".format(eficienciaA/corridas))

	print ("Estadísticas de B")
	
	print ("Tamaño promedio de la cola en B: {:.2f}".format(tamPromColaB/corridas))
	print ("Tiempo promedio de permanencia de las llamadas que llegaron a B: {:.2f}".format(tiempoSisB/corridas))
	print ("Tiempo promedio en cola de llamadas que llegaron a B: {:.2f}".format(tiempoPromColaB/corridas))
	print ("Eficiencia del sistema con las llamadas que llegaron a B: {:.2f}".format(eficienciaB/corridas))

	print ("Tiempo promedio de permanencia de las llamadas que llegaron de A a B: {:.2f}".format(tiempoSisDes/corridas))
	print ("Tiempo promedio en cola de llamadas que llegaron desde A a B: {:.2f}".format(tiempoPromColaDes/corridas))
	print ("Eficiencia del sistema con las llamada que llegaron desde A a B: {:.2f}".format(eficienciaAaB/corridas))
	print ("Porcentaje de llamadas perdidas: {:.2f}%".format(porcentajePerdidas/corridas))

	print ("------------------------------")

def main():
	
	global colaDesviadas
	os.system('cls' if os.name == 'nt' else 'clear')
	
	# se imprime en pantalla todo lo necesario para que el usuario ingrese los datos para iniciar simulación
	print("------------------------------")
	numeroCorridas = int(input("Ingrese la cantidad de corridas de la simulacion: "))
	maximoSimulacion = int(input("Ingrese el tiempo maximo para correr la simulacion (segundos): "))
	delay = input("¿Desea ver la simulacion correr en modo lento? (si/no): ")
	print("------------------------------")

	corridas = numeroCorridas

	# while loop el cual va a realizar n simulaciones dependiendo de la cantidad de simulaciones que quiera el usuario
	while numeroCorridas > 0:

		ruteA = ruteadorA()
		ruteB = ruteadorB()
		reloj = 0
		terminaCorrida = False

		# while loop el cual no terminará hasta que el reloj pase el máximo de tiempo
		while True:

			# se escoge el evento mínimo de nuestra lista de eventos y se procede a ejecutar el que haya salido
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

			# si entra a esta condicion, significa que el reloj ya pasó o es igual al tiempo máximo
			# el siguiente bloque de código imprime estadísticas 
			if terminaCorrida:

				arrayA = ruteA.generarEstadisticas()
				ruteB.actualizarUltimoValorCola(reloj)
				arrayB = ruteB.generarEstadisticas(ruteA.getLlamadasLocales(), reloj)
				
				promedioDepromedios(arrayA, "A")
				promedioDepromedios(arrayB, "B")

				break

			# condición que controla el delay
			if delay == "si":
				
				time.sleep(3)

			# conjunto de contadores que se imprimen cada evento
			print ("Reloj actual del sistema: {:.2f}".format(reloj))
			print ("Evento que se acaba de procesar: " + evento + "\n")

			ruteA.imprimirRuteadorA()
			ruteB.imprimirRuteadorB()

			print ("------------------------------")

		numeroCorridas -= 1

		if numeroCorridas > 0:

			time.sleep(5)
			print ("La siguiente simulación está a punto de comenzar en 5 segundos.")
			time.sleep(5)

		else:
			
			# si entra a este else, significa que la simulación y todas las corridas terminaron
			# entonces imprime el promedio de los promedios
			print ("A continuación se presentan los promedios de todas las corridas anteriores:\n")
			time.sleep(3)
			imprimirPromedios(corridas)
			time.sleep(10)
			
		# termina una corrida, entonces reinicia los valores de los eventos
		eventos["E1"] = 0
		eventos["E2"] = 0
		eventos["E3"] = [1000000000]
		eventos["E4"] = 1000000000
		eventos["E5"] = 1000000000
		colaDesviadas = []

main()
