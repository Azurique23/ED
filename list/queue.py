class Node:
	def __init__(self, valor):
		self.valor = valor
		self.next = None

class Queue:

	def __init__(self):
		self.first:Node = None
		self.last:Node = None
		self.lenght = 0
		

	def inserir(self, no):
		if(self.last != None and self.first != None):
			self.last.next = no
			self.last = no
		else:
			self.last = no
			self.first = no

		self.lenght += 1

	def imprimir(self):
		show = self.first;
		index = 1
		while show:
			print(index,"-", show.valor)
			show = show.next;
			index += 1

	def remover(self):
		if(self.first):
			self.first = self.first.next
			self.lenght -= 1
		else:
			print ("Fila vázia")

	# def remover(self, posicao):
	# 	if(posicao > self.lenght or posicao <= 0):
	# 		print("Posição de entrada invélida")
	# 	else:
	# 		for i in range(1,posicao):
	# 			self.first = self.first.next

	# 		self.lenght = self.lenght-posicao 
	# 		self.first = self.first.next
			
			
# Criando nós
no1 = Node("Primeiro")
no2 = Node("Segundo")
no3 = Node("Terceiro")
no4 = Node("Quarto")

# Criando uma fila
fila = Queue()

# Inserindo valores a fila
fila.inserir(no1)
fila.inserir(no2)
fila.inserir(no3)
fila.inserir(no4)

# Mostrando todos os valores da fila
fila.imprimir()

# Removendo o segundo elemento da vila
fila.remover()
fila.remover()

print("\n------------Após a remoção----------")

# Mostrando a fila após a remoção
fila.imprimir()
