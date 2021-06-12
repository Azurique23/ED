import logging
import time
import random
from typing import NoReturn


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


class Tree(object):
    def __init__(self) -> int:
        self.root:Node = None
        self.lenght:int = 0
        self.height:int = 0
        self.biggest:int = 0
        self.lowest: int = 0

    def put(self, *args:int) -> None:
       
        if not(self.root):
            node = Node(args[0])
            self.root = node
            logger.info("O node com o valor %i é a raíz da árvore.", args[0])
            self.lenght += 1
            self.height = 1
            self.biggest = self.root.value
            self.lowest = self.root.value
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
            if node.value > self.biggest:
                self.biggest = value
            if node.value < self.lowest:
                self.lowest = value
    
    def put_recursive(self, *args:int) -> None:
        nodo: Node; dad: Node
        if not(self.root):
            self.root = Node(args[0])
            logger.info(f"O nó {self.root.value} foi adicionado como raiz da árvore.")
            self.lenght += 1
            self.height = 1
            self.biggest = self.root.value
            self.lowest = self.root.value
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
                if node.value > self.biggest:
                    self.biggest = value
                if node.value < self.lowest:
                    self.lowest = value
                
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

            else:
                self.root = nodereplace

        node: Node = self.root
        if not(self.root):
            print("A árvore está vázia.")
            return
        for node in self.travel(self.root, value): pass

        if node.value != value:
            print ("Nó %i não está na árvore." % (value))
            return

        if node.degree == 0:
            logger.info("O nó %s é uma folha", repr(node))
            if node.dad: node.dad.degree -= 1
            replace(node)

        elif node.degree == 1:
            logger.info("O nó %s é de grau 1", repr(node))
            nodereplace = node.right if node.right else node.left
            node.left = nodereplace.left
            node.right = nodereplace.right
            node.degree = nodereplace.degree + 1
            replace(node, nodereplace)

        else:
            logging.info("O nó %s é de grau 2", repr(node))
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

            if nodereplace != node.left and not(nodereplace.left):
                nodereplace.dad.right = None

            replace(node, nodereplace)

        del node
        self.lenght -= 1
        self.update_height_level_biggest_lowest()
        print("Nó {} foi removido.".format(value))
    
    def pop_recursive(self, value: int) -> str:
        def travel_right(node:Node):
            if node.right:
                return travel_right(node.right)
            return node

        nodereplace: Node
        node: Node = self.root
        if not node:
            print("A árvore está vazia.")
            return
        _, node, __ =self.travel_recursive(node, value)

        if not node:
            print(f"O nó {value} não existe.")
            return

        if node.degree == 0:
            logger.info(f"O nó {value} é uma folha.")
            if node.dad:
                if node.dad.left == node:
                    node.dad.left = None
                else:
                    node.dad.right = None
                node.dad.degree -= 1
            else:
                self.root = None
        elif node.degree == 1:
            logger.info(f"O nó {value} é de grau 1.")
            nodereplace = node.right if node.right else node.left
            if node.dad:
                nodereplace.dad = node.dad
                if node.dad.right == node:
                    node.dad.right = nodereplace
                else:
                    node.dad.left = nodereplace
            else:
                nodereplace.dad = None
                self.root = nodereplace
            nodereplace.level = node.level

        else:
            logger.info(f"O nó {value} é de grau 2.")
            nodereplace =  travel_right(node.left)

            nodereplace.level = node.level
            if nodereplace == node.left:
                if node.right:
                    node.right.dad = nodereplace
                    nodereplace.right = node.right
                nodereplace.degree = 2 if nodereplace.left else 1

                if node.dad: 
                    if  node.dad.left == node:
                        node.dad.left = nodereplace
                    else:
                        node.dad.right = nodereplace
                    nodereplace.dad = node.dad
                else:
                    self.root = nodereplace
            else:
                if nodereplace.left:
                    nodereplace.dad.right = nodereplace.left
                    nodereplace.dad.right.dad = nodereplace.dad
                else:
                    nodereplace.dad.right = None
                    nodereplace.dad.degree -= 1

                nodereplace.degree = node.degree

                node.right.dad = node.left.dad  = nodereplace
                
                nodereplace.right = node.right
                nodereplace.left = node.left
                nodereplace.dad = node.dad

                if node.dad:
                    if node.dad.right == node:
                        node.dad.right = nodereplace
                    else:
                        node.dad.left = nodereplace
                else:
                    self.root = nodereplace

            
        del node
        print(f"O nó {value} foi removido.")
        self.lenght -= 1
        self.update_height_level_biggest_lowest_recursive()

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

    def update_height_level_biggest_lowest(self) -> int:
        height = 0
        lowest = self.root.value if self.root else 0
        biggest = self.root.value if self.root else 0

        node: Node
        for node in self.travel(self.root):
            node.level = node.dad.level+1 if node.dad else 0       
            if node.level >= height:
                height = node.level+1
            if node.value > biggest:
                biggest = node.value
            if node.value < lowest:
                lowest = node.value

        self.height = height
        self.lowest = lowest
        self.biggest = biggest

    def update_height_level_biggest_lowest_recursive(self) -> None:
        def update_height_bigest_lowest_recursive(node:Node) -> None:
        
            if node.right:
                node.right.level = node.level + 1
                update_height_bigest_lowest_recursive(node.right)
            if node.left:
                node.left.level = node.level + 1
                update_height_bigest_lowest_recursive(node.left)

            if node.level >= self.height:
                self.height = node.level+1
            if node.value > self.biggest:
                self.biggest = node.value
        
        self.height = 0
        self.lowest = 0
        self.biggest = 0

        if self.root:
            self.biggest = self.root.value
            self.lowest = self.root.value
            update_height_bigest_lowest_recursive(self.root)
        
    def indentation(self) -> str:
        output = f"ALTURA:{self.height} QUANTIDADE DE NODE: {self.lenght}"
        node: Node
        for node in self.travel(self.root):
            indent = "\t"*node.level
            output += "\n"+indent+"|valor -> "+str(node.value)+"|"

        return output

    def __str__(self)-> str:
        width = self.tree_width(self.height)
        value_width = len(str(self.biggest)) if len(str(self.biggest)) > 1 else 2

        lines = [[" "*(value_width) for __ in range(width)] for _ in range(self.height)]

        def travel(node: Node, position:int, width: int):
            position = position + width
            width = int(abs(width)/2)
            line = lines[node.level]
            line[position-1] = ""+("0"+str(node.value)).rjust(value_width) if node.value < 10 else ""+str(node.value).rjust(value_width)
            lines[node.level] = line

            if node.right:
                travel(node.right, position, -width)
            if node.left:
                travel(node.left, position, width)

        if self.root:travel(self.root, 0, int((width+1)/2))
        for key, line in enumerate(lines):
            lines[key] = "".join(line)
        lines = f"ALTURA:{self.height} QUANTIDADE DE NODE: {self.lenght}\n"+"\n".join(lines)
        return lines
    
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

        right = ""
        left = ""

        if value or value == 0:
            path, node = search(node, value)
            if node.value == value:
                return path, node, None
            return path, None, node

        elif sorted:
            if node.right: right = travel(node.right, format="{right}{value}, {left}")
            if node.left :left = travel(node.left, format="{right}, {value}{left}")
            return  right + str(node.value) + left
        else:
            if node.right: right = travel(node.right)
            if node.left:  left  = travel(node.left)

            return str(node.value) + right + left

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

    @staticmethod
    def tree_width(height: int):
        if height <= 1:
            return 1
        return (Tree.tree_width(height-1)*2) + 1

if __name__ == "__main__":
    tree =  Tree()
    tree.put(16, 24, 20, 28, 18, 30, 22, 26, 17, 19, 21, 23, 25, 27, 29, 31)
    tree.put_recursive(8, 4, 12, 2, 6, 1, 3, 5, 7, 10, 14, 9, 11, 13, 15)
    print(tree.travel_recursive(tree.root, sorted=True))
    # tree.pop(16)
    # tree.pop_recursive(17)
    print(tree.indentation())
    print(tree)

