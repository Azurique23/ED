
# Função de busca sequencial
def sequentialSearch(lista, chave):

	for key, i in enumerate(lista):
		if(i == chave):
			return key

	return -1

# Função de busca binária	
def indexMid(t):
	mid = t/2

	if(mid != int(mid)):
		mid += 0.5
	
	return int(mid)-1

def binSearch(lista, chave):
	
	ls = lista[:]

	t = len(ls)

	mid = indexMid(t)
	midReal = mid

	while  t > 0:

		eleMid = ls[mid]

		if(eleMid == chave):
			return midReal

		elif(eleMid > chave):
			ls = ls[:mid]
			t = len(ls)
			mid = indexMid(t)
			midReal = midReal - (t-mid)
						
		else:
			ls = ls[mid+1:]
			t = len(ls)
			mid = indexMid(t)
			midReal = midReal + (mid+1)
	
	return -1

# Função de busca binária utilizando recursividade
def binSearchRec_(lista, chave, index, tam):

	ele = lista[index]
	

	if( ele == chave):
		return index
	elif(tam[0] < 0 or tam[1] < 0):
		return - 1

	elif(ele > chave):
		tam = tam[0]
		mid = int(tam/2)
		index -= mid+1

		if(tam%2 == 0):
			tam =  [mid-1, mid]
		else:
			tam =  [mid, mid]


		return binSearchRec_(lista, chave, index, tam)
	else:

		tam = tam[1]
		mid = int(tam/2)
		index += mid

		if(tam%2 == 0):
			tam =  [mid-1, mid]
		else:
			index += 1
			tam =  [mid, mid]

		return binSearchRec_(lista, chave, index, tam)

def binSearchRec(lista, chave):
	t = len(lista); tam = 0

	if(lista[0] > chave or lista[t-1] < chave):
		return -1

	index = indexMid(t)

	if(t%2 == 0):
		tam = [index, index+1]
	else:
		tam = [index, index]

	return binSearchRec_(lista, chave, index, tam)



lista = [2, 4, 6, 8, 13, 21, 34, 56, 75, 90]
# listaDes = [48, 1, 28, 9, 14, 23, 6, 15, 30, 99]

while True:
	print(lista)
	n = int(input("chave: "))
	print("Busca sequencial:", sequentialSearch(lista, n))
	print("Busca binária:", binSearch(lista, n))
	print("Busca binária com Recursividade:", binSearchRec(lista, n))
	print("---------------------------------------------------------")

