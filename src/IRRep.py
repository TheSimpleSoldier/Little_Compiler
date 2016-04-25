class IRRep:
    def __init__(self):
        self.lastTemp = 1
        self.first = None
        self.last = None

    def getLast(self):
        return self.last

    def addToEnd(self, nextNode):
        if(self.last is None):
            self.first = nextNode
            self.last = nextNode
        else:
            self.last.nextNode = nextNode

        while(self.last.nextNode is not None):
            self.last = self.last.nextNode

    def printIR(self):
        temp = self.first
        while(temp is not None):
            if(len(temp.second) > 0):
                print(temp.opcode + " " + temp.first + " " + temp.second + " " + temp.result)
            else:
                print(temp.opcode + " " + temp.first + " " + temp.result)
            temp = temp.nextNode
    
    def nextTemp(self):
        self.lastTemp += 1
        return "$T" + str(self.lastTemp - 1)

class IRNode:
    def __init__(self, opcode, first, second, result, nextNode, branchNode):
        self.opcode = opcode
        self.first = first
        self.second = second
        self.result = result
        self.nextNode = nextNode
        self.branchNode = branchNode
