class SymbolTable:
    def __init__(self, name, parent):
        self.name = name
        self.variables = []
        self.children = []
        self.parent = parent

    def getValues(self):
        return self.variables

    def clear(self):
        self.variables = []

    def addChild(self, child):
        self.children.append(child)

    def insertChild(self, child, after):
        if after == "":
            self.children.insert(0, child)
            return

        count = 0
        for c in self.children:
            count += 1
            if c.name == after:
                self.children.insert(count, child)
                return
        self.children.append(child)

    def addVariable(self, variable):
        global error, duplicate
        if not self.contains(variable):
            self.variables.append(variable)
        elif not error:
            error = True
            duplicate = variable.name

    def contains(self, variable):
        for var in self.variables:
            if var.name == variable.name:
                return True

        return False

    def containsName(self, name):
        for var in self.variables:
            if var.name == name:
                return True
        return False


    def insertVar(self, variable, varIndex):
        global error, duplicate
        if not self.contains(variable):
            self.variables.insert(varIndex, variable)
        elif not error:
            error = True
            duplicate = variable.name

    def getLength(self):
        return len(self.variables)

    def printSymbolTable(self):
        print "Symbol table " + self.name
        for var in self.variables:
            if (var.hasValue()):
                print "name " + var.name + " type " + var.v_type+ " value " + var.value
            else:
                print "name " + var.name + " type " + var.v_type

        for child in self.children:
            print ""
            child.printSymbolTable()

    def printTableTiny(self):
        for var in self.variables:
            if(var.v_type == "STRING"):
                print "str " + var.name + " " + var.value
            else:
                print "var " + var.name

    def getType(self, name):
        for var in self.variables:
            if(var.name == name):
                return var.v_type
        return None

    def getParent(self):
       return self.parent


    def getValueForVar(self, name):
        for v in self.varaibles:
            if v.name == name:
                return v
        return self.parent.getValueForVar(name)

class Variable:
    def __init__(self, name, v_type):
        self.name = name
        self.v_type = v_type
        self.has_value = False

    def hasValue(self):
        return self.has_value

    def setValue(self, value):
        self.value = value
        self.has_value = True
