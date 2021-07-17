

from test import V


class Vertex():
    data: any
    degree: int
    _outdegree: int
    _indegree: int
    def __init__(self, data = None) -> None:
        self.data = data 
        self.degree = 0
        self._outdegree = 0 
        self._indegree = 0
        self.edges: list[Edge] = []
        self.next: Vertex or None = None

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

    def __str__(self) -> str:
        return f"data: {self.data} grau-entrada: {self.indegree} grau-saída: {self.outdegree}"


class Edge():
    data: any
    adjacent: Vertex
    def __init__(self, adjacent, data = None) -> None:
        self.data = data
        self.adjacent = adjacent

    def __str__(self) -> str:
        return f"data:{self.data} x: {self.start} y: {self.end}"

class Graph():
    order: int
    size: int
    base: None or Vertex
    top: None or Vertex
    def __init__(self) -> None:
        self.base = None
        self.top = None
        self.order = 0
        self.size = 0
    def addVertex(self, data = None):
        v = self.base
        while v:
            if v.data == data:
                return
        if(self.base):
            vertex = Vertex(data)
            self.top.next = vertex
            self.top = vertex
            self.order += 1
        else:
            self.base = self.top = Vertex(data)
            self.order += 1
    def addEdge(self, x, y):
        v = self.base
        vs = (None, None)
        while v:
            if x == v.data:
                vs[0] = v
            if y == v.data:
                vs[1] = v
            if(vs[0] and vs[1]):
                break
        


if __name__ == "__main__":
    v = Vertex(1)
    v.outdegree += 2
    v.outdegree += 1 
    v.indegree += 1 

    print(v.degree, v.indegree, v.outdegree)