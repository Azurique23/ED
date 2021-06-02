import logging
from math import trunc
from os import path, walk
import time
import random


logger = logging.getLogger(__name__)
formatter = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.WARN, format=formatter, datefmt='%H:%M:%S')


class Node(object):
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node = None
        self.right: Node = None
        self.dad: Node = None
        self.level: int = 0
        self.degree: int = 0
        logging.debug("Objeto %s foi criado com value=%i", super(Node, self).__repr__(), value)

    def __str__(self) -> str:
        right_value = self.right.value if self.right else None
        left_value = self.left.value if self.left else None
        # out = f"Valor:{str(self.value).ljust(5)} |  Nivel:{self.level}  |  Grau:{self.degree}  |  Direita:{str(right_value).ljust(5)} |  Esquerda:{str(left_value).ljust(5)}"
        out = f"|  Valor:{self.value}  |  Nivel:{self.level}  |  Grau:{self.degree}  |  Direita:{right_value}  |  Esquerda:{left_value}  |"
        return out

    def __repr__(self) -> str:
        dad = self.dad.value if self.dad else None
        right = self.right.value if self.right else None
        left = self.left.value if self.left else None
        return f"{self.__class__.__name__}(value={self.value}, level={self.level}, degree={self.degree}, dad.value={dad}, right.value={right}, left.value={left})"


class Tree():
    def __init__(self):
        self.root = None
        self.lenght = 0
        self.height = 0

    def put(self, *args:int) -> None:
       
        if not(self.root):
            node = Node(args[0])
            self.root = node
            logger.info("O node com o valor %i é a raíz da árvore.", args[0])
            self.lenght += 1
            self.height = 1
            args = args[1:]

        for value in args:
            try:
                value = int(value)
            except ValueError as error:
                print("O valor deve ser inteiro.")
                continue

            dad = self.root
        
            for n in self.travel(dad, value):
                dad = n

            if dad.value == value:
                print(f"O nó {value} já está na tree")
                continue

            node = Node(value)
            dad.degree += 1
            node.dad = dad
            node.level = dad.level + 1

            if dad.value > value:
                dad.right = node
                logger.info(f"O nó {value} foi colocado a direita do nó {dad.value}")
            else:
                dad.left = node
                logger.info(f"O nó {value} foi colocado a esquerda do nó {dad.value}")


            self.lenght += 1
            if node.level >= self.height:
                self.height = node.level+1
    
    def put_recursive(self, *args:int) -> None:
        nodo: Node; dad: Node
        if not(self.root):
            self.root = Node(args[0])
            logger.info(f"O nó {self.root.value} foi adicionado como raiz da árvore.")
            self.lenght += 1
            self.height = 1
            args = args[1:]

        for value in args:
            try:
                value = int(value)
            except ValueError as error:
                print("O valor deve ser inteiro.")
                continue
            
            _, _, dad = self.travel_recursive(self.root, value)

            if dad:
                node = Node(value)

                if dad.value > value:
                    dad.right = node
                    logger.info(f"O nó {value} foi colocado a direita do nó {dad.value}")
                else:
                    dad.left = node
                    logger.info(f"O nó {value} foi colocado a esquerda do nó {dad.value}")
                node.dad = dad
                dad.degree += 1
                node.level = dad.level + 1

                self.lenght += 1
                if node.level >= self.height:
                    self.height = node.level + 1
                
            else:
                print(f"Nó {value} já existe")

    def pop(self, value: int) -> str:
        def replace(node: Node, nodereplace: Node or None = None) -> None:
            """ 
            O pai do primeiro  argumento terá com filho no mesmo lado do primeiro
            argumento o segundo argumento
            """
            logger.info("O nó %s foi trocado pelo nó %s", node, nodereplace)
            if nodereplace:
                nodereplace.level = node.level
                nodereplace.dad.degree -= 1
                nodereplace.degree = node.degree
                nodereplace.dad = node.dad
                if node.left != nodereplace :nodereplace.left = node.left
                if node.right != nodereplace : nodereplace.right = node.right

                if node.left and node.left !=  nodereplace:
                    node.left.dad = nodereplace
                if node.right and node.right != nodereplace:
                    node.right.dad = nodereplace
            

            if node.dad:
                if node.dad.right == node:
                    node.dad.right = nodereplace
                else:
                    node.dad.left = nodereplace

                if not(nodereplace):node.dad.degree -= 1
            else:
                self.root = nodereplace


        node: Node = self.root
        if not(self.root):
            return "A árvore está vázia."
        for node in self.travel(self.root, value): pass

        if node.value != value:
            return "Nó %i não está na árvore." % (value)

        if node.degree == 0:
            logger.info("O nó %s é uma folha", repr(node))
            replace(node)

        elif node.degree == 1:
            logger.info("O nó %s é de grau 1", repr(node))
            nodereplace = node.right if node.right else node.left
            node.left = nodereplace.left
            node.right = nodereplace.right
            node.degree = nodereplace.degree + 1
            replace(node, nodereplace)
            self.update_childs_level(nodereplace)

        else:
            logging.info("O nó %s é de grau 2", repr(node))
            
            if node.left:
                nodereplace = node.left

                while nodereplace:
                    if nodereplace.right == None:
                        break
                    nodereplace = nodereplace.right

                if nodereplace.left:
                    if nodereplace.dad != node:
                        nodereplace.dad.degree += 1
                        nodereplace.dad.right = nodereplace.left
                        nodereplace.left.dad = nodereplace.dad
                    else:
                        node.degree += 1
                        nodereplace.level -= 1
                    
                    self.update_childs_level(nodereplace.left)
            
                if nodereplace != node.left and not(nodereplace.left):
                    nodereplace.dad.right = None

                replace(node, nodereplace)

            else:
                nodereplace = node.right

                while nodereplace:
                    if nodereplace.left == None:
                        break
                    nodereplace = nodereplace.left

                if nodereplace.right:
                    if nodereplace.dad != node:
                        nodereplace.dad.degree += 1
                        nodereplace.dad.left = nodereplace.right
                        nodereplace.right.dad = nodereplace.dad
                    else:
                        node.degree += 1
                        nodereplace.level -= 1

                    self.update_childs_level(nodereplace.right)

                if nodereplace != node.right and (not nodereplace.right):
                    nodereplace.dad.left = None

                replace(node, nodereplace)

        del node
        self.lenght -= 1
        self.update_height()
        return "Nó {} removido".format(value)
    
    def pop_recursive(self, value: int) -> str:
        pass

    def search(self, value):
        node: Node
        trace = ""
        for node in self.travel(self.root, value):
            if node.value != value:
                trace += f"{node.value} -> "

        if node.value == value:
            return trace+str(node)
        return "O nó com valor {} não foi encontrado".format(value)

    def searchAB(self, a: int, b : int) -> str:
        n:Node
        nodea: Node or None = None
        nodeb: Node or None = None
        node:Node
        trace = ""

        # Buscando um node em comum
        for node in self.travel(self.root, a):
            value = node.value
            if value == a:
                nodea = node
                break
            elif value == b:
                nodeb = node
                break
            elif (value > a and value < b) or  (value < a and value > b) :
                break

        if nodea:
            if a == b:
                return f"A:B: {nodea}"
            logger.info("B:%i é filho de A:%i", b, a)
            path = ""
            node = None
            if nodea.value > b:
                if nodea.right: node = nodea.right
            else:
                if nodea.left: node = nodea.left

            
            for n in self.travel(node, b):
                if n.value == b:
                    nodeb = n
                    break
                path += f" -> {n.value}"
            if nodeb:
                return f"A:{nodea}{path} -> {nodeb}"
            return f"O nó B:{b} não existe."

        elif nodeb:
            logger.info("A:%i é filho de B:%i", a, b)
            path = ""
            node = None
            if nodeb.value > a:
                if node.right:
                    node = nodeb.right
            else:
                if node.left:
                    node = nodeb.left

            for n in self.travel(node, a):
                if n.value == a:
                    nodea = n
                    break
                path += f" -> {n.value}"
            if nodea:
                return f"B:{nodeb}{path} -> A:{nodea}"
            return f"O nó A:{a} não existe."
        else:
            path = ""
            if node:
                logger.info("A:%i e B:%i são filhos de %i", a, b, node.value)
                if node.value > a:
                    if node.right:
                        for n in self.travel(node.right, a):
                            if n.value == a:
                                nodea = n
                                break
                            path += f" -> {n.value}"
                    path += f" -> {node.value}"
                    if node.left:
                        for n in self.travel(node.left, b):
                            if n.value == b:
                                nodeb = n
                                break
                            path += f" -> {n.value}"
                    if nodea:
                        if nodeb: 
                            return f"A:{nodea}{path} -> B:{nodeb}"
                        return f"O nó B:{b} não existe."

                else:
                    if node.right:
                        for n in self.travel(node.right, b):
                            if n.value == b:
                                nodeb = n
                                break
                            path += f" -> {n.value}"
                    path += f" -> {node.value}"
                    if node.left:
                        for n in self.travel(node.left, a):
                            if n.value == a:
                                nodea = n
                                break
                            path += f" -> {n.value}"
                    if nodea:
                        if nodeb: 
                            return f"B:{nodeb}{path} -> A:{nodea}"
                        return f"O nó B:{b} não existe."

                if not nodeb  and not nodea:
                    return f"O nó A:{a} e B:{b} não existem."

                return f"O nó A:{a} não existe."
            
            return f"O nó A:{a} e B:{b} não existe."

    def search_recursive(self, value: int) -> str:
        node: Node

        path, node, _ =  self.travel_recursive(self.root, value)
        
        if node:
            return f"{path}{node}"

        return "O nó com valor {} não foi encontrado".format(value)
    
    def searchAB_recursive(self, a:int, b:int) -> str:
        fnode: Node
        lnode: Node
        def search(node:Node, a:int, b:int) -> str or Node or None:
            if (node.value > a) == (node.value > b) and not((node.value == a) or (node.value == b)):
                if node.value > a:
                    if node.right: 
                        return search(node.right, a, b)
                else:
                    if node.left: 
                        return search(node.left, a, b)
                return None, "", None

            elif node.value == a:
                nodeb = None
                pathb = ""
                if node.value > b:
                    if node.right:
                        pathb, nodeb, _ = self.travel_recursive(node.right, b)
                else:
                    if node.left:
                        pathb, nodeb, _ =  self.travel_recursive(node.left, b)
                return node, pathb , nodeb

            elif node.value == b:
                nodea = None
                patha = ""
                if node.value > a:
                    if node.right:
                        patha, nodea, _ = self.travel_recursive(node.right, a)
                else:
                    if node.left:
                        patha, nodea, _ = self.travel_recursive(node.left, a)
                return node, patha, nodea
            else:
                nodea = nodeb = None
                patha = pathb = ""
                if node.value > a:
                    if node.right:
                        patha, nodea, _ = self.travel_recursive(node.right, a)
                    if node.left:
                        pathb, nodeb, _ = self.travel_recursive(node.left, b)
                else:
                    if node.right:
                        pathb, nodeb, _ = self.travel_recursive(node.right, b)
                    if node.left:
                        patha, nodea, _ = self.travel_recursive(node.left, a)
                return  nodeb, pathb +f"{node.value} -> "+ patha, nodea
        
        fnode, path, lnode = search(self.root, a, b)

        if b == a and fnode:
            return f"A:B: {fnode}"

        if fnode:
            if fnode.value == b:
                if lnode:
                    return f"B:{fnode} -> {path}A:{lnode}"
                return f"O nó A:{a} não existe"
            if lnode:
                return f"A:{fnode} -> {path}B:{lnode}"
            return f"O nó A:{b} não existe"
        if lnode:
            if lnode.value == a:
                return f"O nó B:{b} não existe"
            return f"O nó A:{a} não existe"
        return f"O nó A:{a} e B:{b} não existem"

    def update_height(self) -> int:
        height = 0
        node: Node
        for node in self.travel(self.root):       
            if node.level >= height:
                height = node.level+1

        self.height = height

        return height

    def update_height_recursive(self) -> None:
        def update_height(node:Node) -> None:
            # logger.info(f"Passando pelo nó {node}")
            if node.right:
                update_height(node.right)
            if node.left:
                update_height(node.left)

            if node.level >= self.height:
                self.height = node.level+1
        
        self.height = 0
        if self.root:
            update_height(self.root)

    def __str__(self) -> str:
        output = f"ALTURA:{self.height} QUANTIDADE DE NODE: {self.lenght}"
        node: Node
        for node in self.travel(self.root):
            indent = "\t"*node.level
            output += "\n"+indent+"|valor -> "+str(node.value)+"|"

        return output

    def show(self)-> str:
        global indent_root
        root = self.root
        indent_root = 0

        def travel(node: Node, right=True, indent = 0):
            global indent_root
            
            wr = 1; wl = 1
            if indent_root > indent:
                indent_root = indent

            if node.right:
                _, wr = travel(node.right, True, indent-1)
            if node.left:
                _, wl = travel(node.left, False)
            width = wr+wl
            return (-wr, wl), width

        def indenter(node: Node, indent):
            r = l =[]
            if node.right:
                r = indenter(node.right, indent - 1) 
            if node.left:
                l =  indenter(node.left, indent + 1)

            return r + [(node.value, node.level, indent)] + l
        

        rindent, lindent = travel(self.root)[0]
        nsir = []
        nsil = []
        lines = [["", 0] for _ in range(self.height)]
        indent_root = -indent_root-rindent

        if root.right: nsir = indenter(self.root.right, rindent) 
        if root.left: nsil = indenter(self.root.left, lindent)

        nodes_indent = nsir+nsil
        lines[0] = ("    "*indent_root)+ f"{root.value}"

        for node in nodes_indent:
            print(node)
            line = lines[node[1]]
            indent = node[2]+(indent_root-line[1])
            line[1] = indent
            line[0] += ("    "*indent)+ f"{node[0]}"
            lines[node[1]] = line

        print(lines[0])

        for line in lines[1:]:
            print(line[0])
    
    def show_tree_recursive(self) -> str:
        pass
    
    @staticmethod
    def travel(node: Node, value=None) -> Node:
        if not(isinstance(node, Node)):
            return None
        if value:
            # logging.info("Buscando o nó %i em travel", value)
            while node:
                # logger.info(f"Passando pelo nó {node}")
                yield node
                if node.value == value:
                    break
                if node.value < value:
                    node = node.left
                else:
                    node = node.right

        else:
            root = node
            save = True
            toright = True
            toleft = True
            while toleft or (node != root):
                # time.sleep(1)
                # logger.info(f"Passando pelo nó {node}")
                if save:
                    yield node
                save = True
                if node.right and toright:
                    node = node.right
                    toright = True
                    
                elif node.left and toleft:
                    toright = True
                    node = node.left
                else:
                    if node == root:
                        break
                    toleft = True if node == node.dad.right else False
                    # if not(node.left):
                    #     yield node
                    # yield node
                    toright = False
                    save = False
                    node = node.dad

    @staticmethod
    def travel_recursive(node: Node, value:int or None=None, sorted:bool=False) -> str or Node :
 
        def travel(node: Node, format:str=" -> {value}{right}{left}") -> str and str:
            r = l = ""
            if node.right:
                r = travel(node.right, format)
            if node.left:
                l = travel(node.left, format)
        
            return format.format(value=node.value, right=r, left=l)
        
        def search(node:Node, value: int) -> str and Node or None:
            
            if node.value == value:
                return "" , node
            if node.value > value:
                if node.right:
                    s, n = search(node.right, value)
                    return f"{node.value} -> {s}", n
            else:
                if node.left:
                    s, n = search(node.left, value)
                    return f"{node.value} -> {s}", n
            return "", node

        if value or value == 0:
            path, node = search(node, value)
            if node.value == value:
                return path, node, None
            return path, None, node

        elif sorted:
            return travel(node.right, format="{right}{value} -> {left}") + str(node.value) + travel(node.left, format="{right} -> {value}{left}")
        else:
            return str(node.value) + travel(node.right) + travel(node.left)

    @staticmethod
    def update_childs_level(node: Node) -> None:
        """
        Deve ser garantido que o pai do nó deve possui o nivel correto.
        """
        if node.dad:
            node.level = node.dad.level + 1
        else: 
            node.level = 0
        if node.left:
            Tree.update_childs_level(node.left)
        if node.right:
            Tree.update_childs_level(node.right)



if __name__ == "__main__":
    tree =  Tree()
    tree.put(1,2,3,4,5,6)
    # tree.put_recursive(8, 3, 1, 6, 4, 7, 10, 14, 15)
    tree.show()
    