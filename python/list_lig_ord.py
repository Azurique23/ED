__author__ = "Marcos Pacheco"

class Node:
    def __init__(self, value):
        self.value = int(value)
        self.prev = None
        self.next = None


class Stack:
    def __init__(self):
        self.esp = None  #Top do stack
        self.ebp = None  #Base do stack
        self.crec = True
        self.lenght = 0

    def push(self, value):
        node = Node(value)

        if(self.esp):
            if(self.crec == (value < self.ebp.value) or value == self.ebp.value):
                node.next = self.ebp
                self.ebp.prev = node 
                self.ebp = node
            elif(self.crec == (value > self.esp.value) or value == self.esp.value):
                node.prev = self.esp
                self.esp.next = node
                self.esp = node
            else:
                p = self.ebp
                while p:
                    if(self.crec == (value < p.value) or value == p.value):
                        node.next = p
                        node.prev = p.prev
                        node.prev.next = node
                        node.next.prev = node
                        break
                    p = p.next
        else:
            self.esp = node
            self.ebp = node            
        
        self.lenght += 1
        
    
    def pop(self, value):
        if(self.ebp):

            if(self.crec): t = self.ebp.value <= value and self.esp.value >= value
            else: t = self.ebp.value >= value and self.esp.value <= value

            if(t and self.lenght <= 1):
                self.ebp = None
                self.esp = None
                self.lenght = 0
                return 0

            p = self.ebp
            while t:
                
                if(p.value == value):
                    if(p.prev and p.next):
                        p.next.prev = p.prev
                        p.prev.next = p.next
                    if(not p.prev):
                        self.ebp = p.next
                        self.ebp.prev = None
                    
                    if(not p.next):
                        self.esp = p.prev
                        self.esp.next = None

                    self.lenght -= 1
                    break

                p = p.next
            
        
    def show(self):
        p = self.ebp
        while p:
            print(p.value)
            p = p.next
    
    def reverse(self):
        if(self.lenght > 1):
            p = self.ebp
            s = p.next
            p.next = None
            p.prev = s
            p = s
            while p.next:
                s = p.next
                p.next = p.prev
                p.prev = s
                p = s
            p.next = p.prev
            p.prev = None

            self.esp = self.ebp
            self.ebp = p

        self.crec = not(self.crec)
        
        
        
            
stack = Stack()

stack.push(1)
stack.push(3)
stack.push(2)
stack.reverse()
stack.show()
stack.reverse()
stack.show()