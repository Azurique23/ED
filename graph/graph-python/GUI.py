from graph import Graph, Vertex, Edge, Stack, Queue, Node
from tkinter import *
from tkinter.ttk import *
import re
from random import randint
import time


class App(Tk, Graph):
    bg_default = "#e6ecf0"
    cw = 0
    ch = 0
    raio = 20
    current_after = None

    widgets: dict[str, Label] = {}

    def __init__(self):
        super().__init__()
        super(Tk, self).__init__()

        self.title("Marcos Pacheco GRAPHS")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.minsize(int(screen_width*0.8), int(screen_height*0.8))
        self.state('normal')

        self.style = Style()

        self.vertex_input = StringVar()
        self.edge_input = StringVar()
        self.graph_order = StringVar(value="ORDEM: 0")
        self.graph_size = StringVar(value="TAMANHO: 0")
        self.search_input = StringVar()
        self.vtx_data = StringVar(value="Dado: ")
        self.vtx_degree = StringVar(value="Grau: ")
        self.vtx_indegree = StringVar(value="Grau-entrada: ")
        self.vtx_outdegree = StringVar(value="Grau-saída: ")

        self.create_styles()
        self.create_frames()
        self.create_widgets()
        self.create_canvas()
        self.context_ = self.drawGraph

    def create_styles(self):

        self.style.configure("TFrame", background=self.bg_default)
        self.style.configure("TT.TLabel", font=(
            'Robot', 22, "bold italic"), background=self.bg_default)
        self.style.configure("OS.TLabel", font=(
            'arial', 11), background="white")
        self.style.configure('TLabel', font=(
            'arial', 15, 'bold'), background=self.bg_default)
        self.style.configure("Entry", font=("Arial", 13))
        self.style.configure('TButton', font=('arial', 13))

        self.style.configure('VG.TButton', font=('arial', 10, "bold"), foreground="#8F09F6")
        self.style.configure('LG.TButton', font=('arial', 10, "bold"), foreground="#940629")

        self.style.configure('AV.TButton',  foreground="#0a2194")
        self.style.configure('AE.TButton',  foreground="#bf5d08")

        self.style.configure('DFS.TButton', font=('arial', 10, "bold"), foreground="#007C27")
        self.style.configure('BFS.TButton', font=('arial', 10, "bold"), foreground="#245724")

    def update_style_880(self):
        self.style.configure("TFrame", background=self.bg_default)
        self.style.configure("TT.TLabel", font=('Robot', 18, "bold italic"))
        self.style.configure("OS.TLabel", font=('Arial', 10))
        self.style.configure('TLabel', font=(
            'Arial', 13, 'bold'), background=self.bg_default)
        self.style.configure("Entry", font=("Arial", 11))
        self.style.configure('TButton', font=('Arial', 9))
        self.style.configure('AC.TButton', font=('Arial', 9), background="red")

    def create_frames(self):
        self.left_frame = Frame(self, padding=(10, 30, 10, 10))
        self.left_frame.place(relheight=1, relwidth=0.2)

        self.right_frame = Frame(self, padding=10)
        self.right_frame.place(relheight=1, relwidth=0.8, relx=0.2)

        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.columnconfigure(1, weight=1)

    def create_widgets(self):
        # Labels
        self.widgets["l_title"] = Label(
            self.left_frame, text="Graph Theory", style="TT.TLabel", anchor=CENTER)
        self.widgets["l_order"] = Label(
            self.left_frame, textvariable=self.graph_order, style="OS.TLabel", anchor=W)
        self.widgets["l_size"] = Label(
            self.left_frame, textvariable=self.graph_size, style="OS.TLabel")
        self.widgets["l_addvtx"] = Label(
            self.left_frame, text="INSERIR VÉRTICE", anchor=CENTER)
        self.widgets["l_addedg"] = Label(
            self.left_frame, text="INSERIR ARESTA", anchor=CENTER)
        self.widgets["l_search"] = Label(
            self.left_frame, text="BUSCA", anchor=CENTER)
        self.widgets["l_info"] = Label(
            self.left_frame, text="VÉRTICE INFORMAÇÕES", anchor=CENTER)
        self.widgets["l_data"] = Label(
            self.left_frame, textvariable=self.vtx_data, style="OS.TLabel", anchor=W)
        self.widgets["l_degree"] = Label(
            self.left_frame, textvariable=self.vtx_degree, style="OS.TLabel")
        self.widgets["l_indegree"] = Label(
            self.left_frame, textvariable=self.vtx_indegree, style="OS.TLabel")
        self.widgets["l_outdegree"] = Label(
            self.left_frame, textvariable=self.vtx_outdegree, style="OS.TLabel")

        # Inputs
        self.widgets["e_vtx"] = Entry(
            self.left_frame, textvariable=self.vertex_input)
        self.widgets["e_vtx"].focus()
        self.widgets["e_vtx"].bind("<Return>", self.c_add_vertices)
        self.widgets["e_edg"] = Entry(
            self.left_frame, textvariable=self.edge_input)
        self.widgets["e_edg"].bind("<Return>", self.c_add_edges)
        self.widgets["e_search"] = Entry(
            self.left_frame, textvariable=self.search_input)

        # Buttons
        self.widgets["b_viewgraph"] = Button(
            self.left_frame, text="Ver grafo", cursor="hand2", command=self.drawGraph, style="VG.TButton")
        self.widgets["b_cleargraph"] = Button(
            self.left_frame, text="Limpar grafo", cursor="hand2", command=self.clearGraph, style="LG.TButton")

        self.widgets["b_addvtx"] = Button(
            self.left_frame, text="ADD Vértice(s)", cursor="hand2", command=self.c_add_vertices, style="AV.TButton")
        self.widgets["b_addedg"] = Button(
            self.left_frame, text="ADD Aresta(s)", cursor="hand2", command=self.c_add_edges, style="AE.TButton")
        self.widgets["b_dfs"] = Button(
            self.left_frame, text="Profundidade", cursor="hand2", command=self.c_dfs, style="DFS.TButton")
        self.widgets["b_bfs"] = Button(
            self.left_frame, text="Largura", cursor="hand2", command=self.c_bfs, style="BFS.TButton")

        # Layout
        self.widgets["l_title"].grid(
            row=0, column=0, sticky="nsew", columnspan=2)

        self.widgets["b_viewgraph"].grid(
            row=1, column=0, sticky="nsew")
        self.widgets["b_cleargraph"].grid(
            row=1, column=1, sticky="nsew")

        self.widgets["l_size"].grid(row=2, column=1, sticky=NSEW)
        self.widgets["l_order"].grid(row=2, column=0, sticky=NSEW)

        self.widgets["l_addvtx"].grid(
            row=3, column=0, sticky="nsew", columnspan=2)
        self.widgets["e_vtx"].grid(
            row=4, column=0, sticky="nsew", columnspan=2)
        self.widgets["b_addvtx"].grid(
            row=5, column=0, sticky="nsew", columnspan=2)

        self.widgets["l_addedg"].grid(
            row=6, column=0, sticky="nsew", columnspan=2)
        self.widgets["e_edg"].grid(
            row=7, column=0, sticky="nsew", columnspan=2)
        self.widgets["b_addedg"].grid(
            row=8, column=0, sticky="nsew", columnspan=2)

        self.widgets["l_search"].grid(
            row=9, column=0, sticky="nsew", columnspan=2)
        self.widgets["e_search"].grid(
            row=10, column=0, sticky="nsew", columnspan=2)
        self.widgets["b_dfs"].grid(
            row=11, column=0, sticky="nsew")
        self.widgets["b_bfs"].grid(
            row=11, column=1, sticky="nsew")

        self.widgets["l_info"].grid(
            row=12, column=0, sticky="nsew", columnspan=2)
        self.widgets["l_data"].grid(
            row=13, column=0, sticky="nsew", columnspan=2)
        self.widgets["l_degree"].grid(
            row=14, column=0, sticky="nsew", columnspan=2)
        self.widgets["l_indegree"].grid(
            row=15, column=0, sticky="nsew", columnspan=2)
        self.widgets["l_outdegree"].grid(
            row=16, column=0, sticky="nsew", columnspan=2)

        self.update_manage_widgets()

    def update_manage_widgets(self, m=1):
        pady5 = {"pady": (5*m, 5*m)}
        pady3 = {"pady": (3*m, 3*m)}

        # Layout
        self.widgets["l_title"].grid(pady=(5*m, 10*m))

        self.widgets["l_size"].grid(pady=(10*m, 20*m))
        self.widgets["l_order"].grid(pady=(10*m, 20*m))

        self.widgets["l_addvtx"].grid(**pady5)
        self.widgets["e_vtx"].grid(**pady5)
        self.widgets["b_addvtx"].grid(pady=(5*m, 20*m))

        self.widgets["l_addedg"].grid(**pady5)
        self.widgets["e_edg"].grid(**pady5)
        self.widgets["b_addedg"].grid(pady=(5*m, 20*m))

        self.widgets["l_search"].grid(**pady5)
        self.widgets["e_search"].grid(**pady5)
        self.widgets["b_dfs"].grid(pady=(5*m, 20*m))
        self.widgets["b_bfs"].grid(pady=(5*m, 20*m))

        self.widgets["l_info"].grid(**pady5)
        self.widgets["l_data"].grid(**pady3)
        self.widgets["l_degree"].grid(**pady3)
        self.widgets["l_indegree"].grid(**pady3)
        self.widgets["l_outdegree"].grid(**pady3)

    def canvas_configure_event(self, e: Event):
        if(not hasattr(self, "max_window_width")):
            self.max_window_width = self.winfo_width()
            self.max_window_height = self.winfo_height()

        lw = self.cw
        lh = self.ch

        self.cw, self.ch = e.width, e.height
        self.cmx = self.cw//2
        self.cmy = self.ch//2

        if(self.cw < 880):
            self.raio = 18
            self.update_style_880()
        else:
            self.raio = 20
            self.create_styles()

        v = self.baseVertex

        self.update_manage_widgets(self.winfo_height()/self.max_window_height)

        while v:
            v.x = round((v.x*self.cw)/lw)
            v.y = round((v.y*self.ch)/lh)
            v = v.next
            if(v == self.baseVertex):
                break

        self.context_(0)

    def create_canvas(self):
        self.canvas = Canvas(self.right_frame, bg="#fcfcfc")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Configure>", self.canvas_configure_event)

    def c_add_vertices(self, e=None):
        text_entry = self.vertex_input.get()
        self.vertex_input.set("")
        vertices_data = [datavtx for datavtx in re.split(
            r"(?:[,;\s]+\s*)+", text_entry) if datavtx]

        for data in vertices_data:
            self.addVertex(data)
        self.update_size_order()
        self.drawGraph()

    def c_add_edges(self, e=None):
        text_entry = self.edge_input.get()
        self.edge_input.set("")
        vertices_data = [datavtx for datavtx in re.split(
            r"[,;\s\)\(]+", text_entry)]

        vx = None
        for data in vertices_data:
            if(vx):
                self.addEdge(vx, data)
                vx = None
            else:
                vx = data
        self.update_size_order()
        self.drawGraph()

    def drawQueue(self, node: Node, sleep=700):
        if(isinstance(node.value, Vertex)):
            self.drawVertex(node.value)
        else:
            self.drawEdge(node.value)
        if(node.next):
            self.current_after = self.after(
                sleep, self.drawQueue, node.next, sleep)

    def c_dfs(self, sleep=700):

        if self.current_after:
            self.after_cancel(self.current_after)

        datavi = self.search_input.get()
        order_draw = super().dfs(datavi)

        if(order_draw):
            node = order_draw.base
            self.canvas.delete("all")
            self.context_ = self.c_dfs
            self.drawVertex(node.value, fill="#007C27")
            self.setVtxInfo(node.value)
            if node.next:
                self.current_after = self.after(
                    sleep, self.drawQueue, node.next, sleep)

    def c_bfs(self, sleep=700):
        if self.current_after:
            self.after_cancel(self.current_after)

        datavi = self.search_input.get()
        order_draw = super().bfs(datavi)

        if(order_draw):
            node = order_draw.base
            self.canvas.delete("all")
            self.context_ = self.c_bfs
            self.drawVertex(node.value, fill="#245724")
            self.setVtxInfo(node.value)
            if node.next:
                self.current_after = self.after(
                    sleep, self.drawQueue, node.next, sleep)

    def addVertex(self, data: any):
        v = self.baseVertex
        count = 0
        offset = self.raio*3
        while 1:
            x = randint(self.raio+10, self.cw-(self.raio+10))
            y = randint(self.raio+10, self.ch-(self.raio+10))
            v = self.baseVertex
            while v:
                if((x > v.x-offset and x < v.x+offset) and (y > v.y-offset and y < v.y+offset)):
                    x = y = None
                    break
                v = v.next
                if(v == self.baseVertex):
                    break

            if(x and y):
                break
            if(count > 10000000):
                print("Impossivel adicionar node não tem espaço no canvas.")
                return
            count += 1

        vtx = super().addVertex(data=data)
        if(vtx):
            vtx.x = x
            vtx.y = y

    def drawVertex(self, vtx: Vertex, fill="#0a2194"):
        self.canvas.create_oval(vtx.x-self.raio, vtx.y-self.raio,
                                vtx.x+self.raio, vtx.y+self.raio, fill=fill, outline="")
        self.canvas.create_text(vtx.x, vtx.y, text=vtx.data, fill="white", font=(
            "Arial", int(self.raio/2), "bold"))

    def drawEdge(self, edge: Edge, fill="#bf5d08"):
        def animation(ln, tx, ty, hx, hx_max, s, m,n):
            hy = round((m*hx)+n)
            self.canvas.coords(ln, tx,ty, hx, hy)
            hx = hx+s
            if(s == 1):
                if(hx < hx_max):
                    self.after(10, animation, ln, tx, ty, hx, hx_max, s, m,n)
            else:
                if(hx > hx_max):
                    self.after(10, animation, ln, tx, ty, hx, hx_max, s, m,n)

        if(edge.head == edge.tail):
            v = edge.head
            self.canvas.create_line(((v.x-10, v.y-(self.raio-3)), (v.x-15, v.y-(self.raio + 10)), (v.x, v.y-(
                self.raio + 20)), (v.x+15, v.y-(self.raio + 10)), (v.x+10, v.y-(self.raio-3))),  fill=fill, arrow=LAST)

        else:
            a = edge.head.x-edge.tail.x
            b = edge.head.y-edge.tail.y

            m = (edge.head.y-edge.tail.y)/(edge.head.x-edge.tail.x)
            n = edge.tail.y-(m*edge.tail.x)

            hip = ((a**2)+(b**2))**(1/2)

            offsetx = int((20*a)/hip)
            offsety = int((20*b)/hip)

            tx = edge.tail.x+offsetx
            ty = edge.tail.y+offsety
            hx = edge.head.x-offsetx
            hy = edge.head.y-offsety


            ln = self.canvas.create_line(
                tx, ty, tx, ty, fill=fill, arrow=LAST, width=2, arrowshape=(10, 10, 5), smooth=1)
            if(edge.tail.x > edge.head.x):
                self.after(10, animation, ln, tx, ty, tx, hx, -1, m,n)
            else:
                self.after(10, animation, ln, tx, ty, tx, hx, 1, m,n)

    def drawGraph(self, *args, **kargs):
        if self.current_after:
            self.after_cancel(self.current_after)
        self.canvas.delete("all")
        self.context_ = self.drawGraph
        vtx = self.baseVertex
        edge = self.topEdge

        while edge:
            self.drawEdge(edge)
            edge = edge.nextAll

        while vtx:
            self.drawVertex(vtx)

            vtx = vtx.next
            if(vtx == self.baseVertex):
                break

    def update_size_order(self):
        self.graph_order.set("ORDEM: "+str(self.order))
        self.graph_size.set("TAMANHO: "+str(self.size))

    def clearGraph(self):
        self.baseVertex = None
        self.topVertex = None
        self.topEdge = None
        self.order = 0
        self.size = 0

        self.vtx_data.set(value="Dado: ")
        self.vtx_degree.set(value="Grau: ")
        self.vtx_indegree.set(value="Grau-entrada: ")
        self.vtx_outdegree.set(value="Grau-saída: ")

        self.update_size_order()
        self.drawGraph()

    def setVtxInfo(self, vtx: Vertex):
        self.vtx_data.set("Dado: "+vtx.data)
        self.vtx_degree.set("Grau: "+str(vtx.degree))
        self.vtx_indegree.set("Grau-entrada: "+str(vtx.indegree))
        self.vtx_outdegree.set("Grau-saída: "+str(vtx.outdegree))


if __name__ == "__main__":
    app = App()


    app.mainloop()
