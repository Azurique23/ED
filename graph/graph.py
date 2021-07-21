__author__ = "Marcos Pacheco Uchoa"

class Node():
    value: 'Vertex' or 'Edge'

    def __init__(self, value: 'Vertex') -> None:
        self.value = value
        self.next = None

class Stack():
    top: Node
    def __init__(self) -> None:
        self.top = None

    def push(self, value: 'Vertex' or 'Edge') -> None:
        node = Node(value)

        if(self.top):
            node.next = self.top
            self.top = node
        else:
            self.top = node

    def pop(self) -> Node:
        node = self.top
        self.top = self.top.next if self.top else None

        return node

class Queue(Stack):
    base: Node
    def __init__(self) -> None:
        super().__init__()
        self.base = None

    def push(self, value: 'Vertex') -> None:
        node = Node(value)  
        if(self.top):
            self.top.next = node
            self.top = node
        else:
            self.base = self.top = node

    def pop(self) -> Node:
        node = self.base
        if(self.top == node): 
            self.base = self.top = None
        else:
            self.base = node.next if node else Node
        return node

class Vertex():
    data: any
    degree: int
    _outdegree: int
    _indegree: int
    adjacents: 'Edge' 
    next: 'Vertex' 
    visisted: bool
    level: int

    def __init__(self, data = None) -> None:
        self.data = data 
        self.degree = 0
        self._outdegree = 0 
        self._indegree = 0
        self.adjacents= None
        self.next = None
        self.level = 0
        self.visisted = False
        
    @property
    def outdegree(self):
        return self._outdegree

    @outdegree.setter
    def outdegree(self, a):
        self._outdegree = a
        self.degree = self._outdegree + self._indegree

    @property
    def indegree(self):
        return self._indegree

    @indegree.setter
    def indegree(self, a):
        self._indegree = a
        self.degree = self._outdegree + self._indegree

    def addEdge(self, head:'Vertex', nextAll: 'Edge', data = None ) -> 'Edge' :
        edge =  Edge(self, head, self.adjacents, nextAll, data)
        self.adjacents = edge
        head.indegree  += 1
        self.outdegree += 1
        return edge


    def __str__(self) -> str:
        return f"data: {self.data} grau-entrada: {self.indegree} grau-saída: {self.outdegree} grau: {self.degree}"

class Edge():
    data: any
    next: Vertex
    nextAll: Vertex
    tail: Vertex
    head: Vertex

    def __init__(self, tail: Vertex, head:Vertex, next:'Edge', nextAll:'Edge', data: any = None) -> None:
        self.data = data
        self.tail = tail
        self.head = head
        self.next = next
        self.nextAll = nextAll

    def __str__(self) -> str:
        return f"({self.tail.data}, {self.head.data})"

class Graph():
    order: int
    size: int
    baseVertex: Vertex
    topVertex: Vertex
    topEdge: Edge

    def __init__(self) -> None:
        self.baseVertex = None
        self.topVertex = None
        self.topEdge = None
        self.order = 0
        self.size = 0

    def addVertex(self, data:any = None) -> None or Vertex:
        v = self.baseVertex
        while v:
            if v and v.data == data:
                print("O nó já existe")
                return
            v = v.next
            if(v == self.baseVertex):
                break

        vertex = Vertex(data)
        if(self.baseVertex):
            self.topVertex.next = vertex
            self.topVertex = vertex
            self.topVertex.next = self.baseVertex 
            self.order += 1
        else:
            self.baseVertex = self.topVertex = vertex
            vertex.next = self.baseVertex
            self.order += 1
        return vertex

    def addEdge(self, x: any, y:any, data:any = None) -> None or Edge:
        xvertex: Vertex = None
        yvertex: Vertex = None

        v = self.baseVertex
        while v:
            if(v.data == x):
                xvertex = v
            if(v.data == y):
                yvertex = v
            if(xvertex and yvertex):
                break
            v = v.next
            if(v == self.baseVertex):
                break


        if(xvertex and yvertex):
            e = xvertex.adjacents
            while e:
                if(e.head == yvertex):
                    print(f"A aresta entre os vertices {x} e {y} já existe.")
                    return e
                e = e.next

            edge = xvertex.addEdge(yvertex, self.topEdge, data)

            self.size += 1
            self.topEdge = edge
            return edge

        notexist = (" "+str(y)+" não existe."  if xvertex else False) or (" "+str(x)+" não existe."if yvertex else False) or f"s {y} e {x} não existem"
        print("Vertice"+notexist)

    def dfs(self, datavi, datavo=None)-> Queue:
        def visitV(vertex: Vertex, count: int) -> None or Vertex:
            vertex.visisted = True
            order_visit.push(vertex)
            # print(vertex, f"level: {count}")
            if(vertex.data == datavo):
                return vertex
            
            e = vertex.adjacents
            vertex.level = count
            while e:
                order_visit.push(e)
                if(e.head.visisted == False):
                    target = visitV(e.head, count+1)
                    if(target):
                        return target
                e = e.next

        order_visit = Queue()
        v = self.baseVertex
        vi = None
        while v:
            v.visisted = False
            if(v.data == datavi):
                vi = v
            v = v.next  
            if(v == self.baseVertex):
                break
        if(vi):
            v = vi
            count = 0
            while v:
                if(v.visisted == False):
                    v.visisted = True
                    target = visitV(v, count+1)
                    break
                    if(target):
                        return target
                    count = 0
                v = v.next
                if(v == vi):
                    break
            return order_visit
            print(f"{datavo} não existe;")
        else:
            print(f"O vertice {datavi} não existe.")

    def bfs(self, datavi, datavo=None)-> Queue:
        def visitVs(q:Queue, v: Vertex):
            v.visisted = True
            order_visit.push(v)
            while v:
                count = v.level
                # print(v, f"level: {count}")

                e = v.adjacents
                while e:
                    order_visit.push(e)
                    va = e.head
                    if(not va.visisted):
                        order_visit.push(va)
                        va.visisted = True
                        va.level = count+1
                        q.push(va)
                    e = e.next
                n = q.pop()
                if(n): v = n.value
                else: break


        order_visit = Queue()
        q = Queue()
        v = self.baseVertex
        vi = None
        while v:
            v.visisted = False
            if(v.data == datavi):
                vi = v
            v = v.next  
            if(v == self.baseVertex):
                break
        if(vi):
            v = vi
            count = 0
            while v:
                if(v.visisted == False):
                    v.visisted = True
                    v.level = 1
                    target = visitVs(q, v)
                    break
                    if(target):
                        return target
                    count = 0
                v = v.next
                if(v == vi):
                    break
            return order_visit
            print(f"{datavo} não existe;")
        else:
            print(f"O vertice {datavi} não existe.")

    def __call__(self):
        print(f"ORDEM: {self.order} TAMANHO: {self.size}\n")
        v = self.baseVertex
        while v:
            print(v)
            e = v.adjacents
            if(e):
                print("Arestas:",e, end="")
                e = e.next
                while e:
                    print(",", e, end="")
                    e = e.next

            else: print("Vertice não possui adjacentes")
            
            print("\n")
            v = v.next
            if(v == self.baseVertex): break



if __name__ == "__main__":
    g = Graph()

    for i in range(1, 11):
        g.addVertex(i)


    g.addEdge(1, 2)
    g.addEdge(2, 2)
    g.addEdge(3, 10)
    g.addEdge(7, 6)
    g.addEdge(6, 10)
    g.addEdge(3, 7)
    g.addEdge(4, 2)


    print("BUSCA PROFUNDIDADE")
    g.dfs(3)

    print("BUSCA LARGURA")
    g.bfs(3)
    # g()
