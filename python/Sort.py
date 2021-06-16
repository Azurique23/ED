from random import randint

def selectionSort(ls):
	ls= ls[:]
	menor = 0;indexMenor = 0

	for i in range(0, len(ls)):
		for index in range(i, n):
			valor = ls[index]
			if(valor < menor or index == i):
				menor = valor
				indexMenor = index

		iAnterior= ls[i]
		ls[i] = ls[indexMenor]
		ls[indexMenor] = iAnterior

	return ls

def insertSort(ls):
	ls = ls[:]
	for i in range(1, len(ls)):
		elem = ls[i]
		ls.pop(i)
		for desci in range(i-1,-1,-1):
			if(ls[desci] < elem):
				ls.insert(desci+1, elem)
				break
			if(desci == 0):
				ls.insert(0, elem)

	return ls

def dividiOrdena(ls):
	medio = int(len(ls)/2)
	ls1 = ls[:medio]
	ls2 = ls[medio:]
	
	if(len(ls1) != 1):
		ls1 = dividiOrdena(ls1)
		ls2 = dividiOrdena(ls2)
		c = []
		i1 = 0
		i2 = 0
		lsComp = False; t2= len(ls2)
		while i1<len(ls1):
			if( lsComp or ls1[i1] <  ls2[i2] ):
				c.append(ls1[i1])
				i1+=1
			else:
				c.append(ls2[i2])
				if(i2+1 == t2):
					lsComp = True
				else:
					i2+=1
		if(t2+len(ls1) != len(c)):
			c+= ls2[i2:]
		return c
	else:
		if(ls[0]<ls[1]):
			return ls
		return [ls[1],ls[0]]


def mergeSort(ls):
	t = len(ls)
	if(t!=1):
		ls=ls[:]
		n = 2
		while True:
			if(n == t):
				break
			if(n > t):
				r = n-t
				for i in range(r):
					ls.insert(0, 0)
				break
			n*=2
		ls = dividiOrdena(ls)
		for i in range(r):
			ls.remove(0)

	return ls



def quickSort(ls):
	if(ls != []):
		ls = ls[:]
		t = len(ls)
		pivo = ls[t-1]
		ls.pop(t-1)
		if(t > 1):
			menor = []
			maior = []
			ultimoMaior = 0
			for i in ls:
				if(i <= pivo):
					menor +=[i]
				else:
					maior +=[i]

			if(menor != []):
				menor = quickSort(menor)
			if(maior != []):
				maior = quickSort(maior)

			ls = menor + [pivo] +maior

			return ls
		else:
			ls += [pivo]
			return ls
	else:
		return ls
	
lista= []
n = 20

for t in range(0,n):
    lista.append(randint(0, 50))

print("lista inicial: ",lista)


print("lista ordenada Selection sort: ", selectionSort(lista))
print("lista ordenada Insert sort: ", insertSort(lista))
print("lista ordenada Merge sort: ", selectionSort(lista))
print("Lista Ordenada Quick sort: ", quickSort(lista))


