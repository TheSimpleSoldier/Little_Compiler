class IRRep:
    def __init__(self):
        self.lastTemp = 1
        self.lastLabel = 1
        self.first = None
        self.last = None

    def getLast(self):
        return self.last

    def addToEnd(self, nextNode):
        if(nextNode is not None):
            if(self.last is None):
                self.first = nextNode
                self.last = nextNode
            else:
                self.last.nextNode = nextNode

            while(self.last.nextNode is not None):
                self.last = self.last.nextNode

    def nextTemp(self):
        self.lastTemp += 1
        return "$T" + str(self.lastTemp - 1)

    def nextLabel(self):
        self.lastLabel += 1
        return "label" + str(self.lastLabel - 1)

    def printIR(self):
        temp = self.first
        while(temp is not None):
            if(len(temp.second) > 0):
                print(temp.opcode + " " + temp.first + " " + temp.second + " " + temp.result)
            else:
                print(temp.opcode + " " + temp.first + " " + temp.result)
            temp = temp.nextNode
    
    def printTiny(self, symbolTable):
        temp = self.first
        print(";IR code")
        while(temp is not None):
            if(len(temp.second) > 0):
                print(";" + temp.opcode + " " + temp.first + " " + temp.second + " " + temp.result)
            else:
                print(";" + temp.opcode + " " + temp.first + " " + temp.result)
            temp = temp.nextNode
        temp = self.first
        print(";tiny code")
        #declare variables
        symbolTable.printTableTiny()
        count = 0
        references = {}
        while(temp is not None):
            first = temp.first
            if "$" in first:
                if first in references:
                    first = references[first]
                else:
                    references[first] = "r" + str(count)
                    first = references[first]
                    count += 1
            second = temp.second
            if "$" in second:
                if second in references:
                    second = references[second]
                else:
                    references[second] = "r" + str(count)
                    second = references[second]
                    count += 1
            result = temp.result
            if "$" in result:
                if result in references:
                    result = references[result]
                else:
                    references[result] = "r" + str(count)
                    result = references[result]
                    count += 1
            if(temp.opcode == "STOREI" or temp.opcode == "STOREF"):
                if(first[0] != "r" and result[0] != "r"):
                    compare = "r" + str(count)
                    count += 1
                    print("move " + first + " " + compare)
                    print("move " + compare + " " + result)
                else:
                    print("move " + first + " " + result)
            elif(temp.opcode == "READI"):
                print("sys readi " + temp.first)
            elif(temp.opcode == "READF"):
                print("sys readr " + temp.first)
            elif(temp.opcode == "WRITEI"):
                print("sys writei " + temp.first)
            elif(temp.opcode == "WRITEF"):
                print("sys writer " + temp.first)
            elif(temp.opcode == "WRITES"):
                print("sys writes " + temp.first)
            elif(temp.opcode == "ADDI"):
                print("move " + first + " " + result)
                print("addi " + second + " " + result)
            elif(temp.opcode == "ADDF"):
                print("move " + first + " " + result)
                print("addr " + second + " " + result)
            elif(temp.opcode == "SUBI"):
                print("move " + first + " " + result)
                print("subi " + second + " " + result)
            elif(temp.opcode == "SUBF"):
                print("move " + first + " " + result)
                print("subr " + second + " " + result)
            elif(temp.opcode == "MULTI"):
                print("move " + first + " " + result)
                print("muli " + second + " " + result)
            elif(temp.opcode == "MULTF"):
                print("move " + first + " " + result)
                print("mulr " + second + " " + result)
            elif(temp.opcode == "DIVI"):
                print("move " + first + " " + result)
                print("divi " + second + " " + result)
            elif(temp.opcode == "DIVF"):
                print("move " + first + " " + result)
                print("divr " + second + " " + result)
            elif(temp.opcode == "LABEL"):
                print("label " + first)
            elif(temp.opcode == "JUMP"):
                print("jmp " + first)
            elif(temp.opcode == "GTI" or temp.opcode == "GTF"):
                tstring = "i"
                if(temp.opcode == "GTF"):
                    tstring = "r"
                compare = "r" + str(count)
                count += 1
                print("move " + second + " " + compare)
                print("cmp" + tstring + " " + first + " " + compare)
                print("jgt " + result)
            elif(temp.opcode == "GEI" or temp.opcode == "GEF"):
                tstring = "i"
                if(temp.opcode == "GEF"):
                    tstring = "r"
                compare = "r" + str(count)
                count += 1
                print("move " + second + " " + compare)
                print("cmp" + tstring + " " + first + " " + compare)
                print("jge " + result)
            elif(temp.opcode == "LTI" or temp.opcode == "LTF"):
                tstring = "i"
                if(temp.opcode == "LTF"):
                    tstring = "r"
                compare = "r" + str(count)
                count += 1
                print("move " + second + " " + compare)
                print("cmp" + tstring + " " + first + " " + compare)
                print("jlt " + result)
            elif(temp.opcode == "LEI" or temp.opcode == "LEF"):
                tstring = "i"
                if(temp.opcode == "LEF"):
                    tstring = "r"
                compare = "r" + str(count)
                count += 1
                print("move " + second + " " + compare)
                print("cmp" + tstring + " " + first + " " + compare)
                print("jle " + result)
            elif(temp.opcode == "NEI" or temp.opcode == "NEF"):
                tstring = "i"
                if(temp.opcode == "NEF"):
                    tstring = "r"
                compare = "r" + str(count)
                count += 1
                print("move " + second + " " + compare)
                print("cmp" + tstring + " " + first + " " + compare)
                print("jne " + result)
            elif(temp.opcode == "EQI" or temp.opcode == "EQF"):
                tstring = "i"
                if(temp.opcode == "EQF"):
                    tstring = "r"
                compare = "r" + str(count)
                count += 1
                print("move " + second + " " + compare)
                print("cmp" + tstring + " " + first + " " + compare)
                print("jeq " + result)
            temp = temp.nextNode
        print("sys halt") 

class IRNode:
    def __init__(self, opcode, first, second, result, nextNode, branchNode):
        self.opcode = opcode
        self.first = first
        self.second = second
        self.result = result
        self.nextNode = nextNode
        self.branchNode = branchNode
