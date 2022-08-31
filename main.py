class Node(object):
    def __init__(self, *args, **kwargs):
        self.parent = None
        self.leftChild = None
        self.rightChild = None
        self.key = None
        self.data = None
        self.height = None

    def __str__(self):
        if str(self.data):
            return 'Key: ' + str(self.key) + ' Data: ' + str(self.data)

    def getMax(self):
        if self.rightChild:
            return self.rightChild.getMax()
        else:
            return self

    def getMin(self):
        if self.leftChild:
            return self.leftChild.getMin()
        else:
            return self

    def insert(self, node):
        if type(node) == type(Node()):
            if self.key > node.key:
                if not self.leftChild:
                    self.leftChild = node
                    node.parent = self
                else:
                    node.height += 1
                    self.leftChild.insert(node)
            elif self.key < node.key:
                if not self.rightChild:
                    self.rightChild = node
                    node.parent = self
                else:
                    node.height += 1
                    self.rightChild.insert(node)
            else:
                self.data = node.data
        else:
            print('gimme no shit to eat!')

    def findNodeByKey(self, key):
        if self.key == key:
            return self
        elif self.key > key:
            if self.leftChild:
                return self.leftChild.findNodeByKey(key)
        else:
            if self.rightChild:
                return self.rightChild.findNodeByKey(key)

    def getDescendant(self):
        # black magic...keep eye on!
        if self.rightChild:
            return self.rightChild.getMin()
        y = self.parent

        while y and self == y.rightChild:
            self = y
            y = y.parent
        return y

    def preOrder(self):
        print(self)
        print(self.height)
        if self.leftChild:
            self.leftChild.preOrder()
        if self.rightChild:
            self.rightChild.preOrder()

    def update(self, key, value):
        if self.key == key:
            self.data = value
            return self
        elif self.key > key:
            if self.leftChild:
                return self.leftChild.update(key, value)
        else:
            if self.rightChild:
                return self.rightChild.update(key, value)

    def findByName(self, SearchValue):
        if self:
            if self.data["name"] == SearchValue:
                print(self.data)
            if self.leftChild:
                self.leftChild.findByName(SearchValue)
            if self.rightChild:
                self.rightChild.findByName(SearchValue)


class Tree(object):
    def __init__(self):
        self.root = None
        self.count = 0
        self.search = []

    def getMax(self):
        if self.root:
            return self.root.getMax()
        else:
            print('Tree is empty (brought to you by getMax() (tm))')
            return None

    def getMin(self):
        if self.root:
            return self.root.getMin()
        else:
            print('Tree is empty (brought to you by getMin() (tm))')
            return None

    def findNodeByKey(self, key):
        if self.root:
            return self.root.findNodeByKey(key)
        else:
            return None

    def update(self, key, value):
        if self.root:
            return self.root.update(key, value)
        else:
            return None

    def deleteNodeByKey(self, key):
        if self.root:
            # le smart way
            x = None
            y = None
            n = self.root.findNodeByKey(key)
            if not n.leftChild or not n.rightChild:
                x = n
            else:
                x = n.getDescendant()
            if x.leftChild:
                y = x.leftChild
            else:
                y = x.rightChild
            if y:
                y.parent = x.parent
            if not x.parent:
                self.root = y
            elif x == x.parent.leftChild:
                x.parent.leftChild = y
            else:
                x.parent.rightChild = y
            n.key = x.key
            n.data = x.data
        else:
            return None

    def insert(self, key, data):
        n = Node()
        n.key = key
        n.data = data
        if not self.root:
            self.root = n
            n.height = 0
            self.count += 1
        else:
            n.height = 1
            self.root.insert(n)
            self.count += 1

    def preOrder(self):
        if self.root:
            print(self.root)
            if self.root.leftChild:
                self.root.leftChild.preOrder()
            if self.root.rightChild:
                self.root.rightChild.preOrder()
        else:
            print('No hay nada.')

    def findByName(self, SearchValue):
        if self.root:
            if self.root.data["name"] == SearchValue:
                print(self.root.data)
            if self.root.leftChild:
                self.root.leftChild.findByName(SearchValue)
            if self.root.rightChild:
                self.root.rightChild.findByName(SearchValue)


def main():
    from csv import reader
    import json
    print('Por favor ingrese la direccion del archivo CSV:')
    x = input()

    FileArray = []

    # open file
    with open(x, "r") as my_file:
        file_reader = reader(my_file)
        ArbolDPI = Tree();
        for i in file_reader:
            cont = 1;
            persona = ''
            newObject = {"Operacion": '', "Persona": ''}

            SplitComas = i[0].split(";")
            newObject["Operacion"] = SplitComas[0]
            persona += SplitComas[1] + ","

            while (cont < len(i)):
                AddComas = i[cont].split(":");
                if (len(AddComas) == 2):
                    persona += "\"" + AddComas[0] + "\":" + AddComas[1]
                else:
                    persona += "\"" + AddComas[0] + "\":" + AddComas[1] + ":" + AddComas[2] + ":" + AddComas[3]
                if (cont != len(i) - 1):
                    persona += ","
                cont += 1
            newObject["Persona"] = json.loads(persona)
            FileArray.append(newObject)

        for Object in FileArray:
            if (Object["Operacion"] == "INSERT"):
                ArbolDPI.insert(int(Object["Persona"]["dpi"]), Object["Persona"])
            elif (Object["Operacion"] == "DELETE"):
                ArbolDPI.deleteNodeByKey(int(Object["Persona"]["dpi"]))
            elif (Object["Operacion"] == "PATCH"):
                ArbolDPI.update(int(Object["Persona"]["dpi"]), Object["Persona"])

        while True:
            print('Quieres buscar por DPI o por Nombre?')
            print('')
            print('Escribe D si es por DPI')
            print('Escribe N si es por Nombre')
            Op1 = input()
            if Op1 == 'D' or Op1 == 'd':
                print('')
                print('Solo deben ser numeros')
                x = input()
                print(ArbolDPI.findNodeByKey(int(x)))
            else:
                print('')
                print('Si no se imprime nada en pantalla es por que no hay nodos con ese nombre')
                print('Solo letras minusculas')
                name = input()
                ArbolDPI.findByName(name)

            print('Preciona Enter Para Repetir el proceso')
            input()

if __name__ == '__main__':
    main()