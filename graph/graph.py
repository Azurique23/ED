

class Vertex():
    data: any
    degree: int
    _outdegree: int
    _indegree: int
    adjacents: 'Edge' 
    ext: 'Vertex' 
    def __init__(self, data = None) -> None:
        self.data = data 
        self.degree = 0
        self._outdegree = 0 
        self._indegree = 0
        self.adjacents= None
        self.next = None

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
        return f"data: {self.data} grau-entrada: {self.indegree} grau-saída: {self.outdegree}"


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
            if v.data == data:
                return
            v = v.next

        vertex = Vertex(data)
        if(self.baseVertex):
            self.top.next = vertex
            self.top = vertex
            self.order += 1
        else:
            self.baseVertex = self.top = vertex
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





if __name__ == "__main__":
    g = Graph()

    for i in range(1, 11):
        g.addVertex(i)


    g.addEdge(1, 2)
    g.addEdge(2, 2)
    g.addEdge(3, 2)
    g.addEdge(4, 2)
    g.addEdge(2, 2)

    g()
