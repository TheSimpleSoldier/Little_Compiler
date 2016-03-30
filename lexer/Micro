#!/usr/local/bin/python2.7


import sys
import lex

error = False
duplicate = ""

#All the reserved words
reserved = [
    'PROGRAM',
    'BEGIN',
    'END',
    'FUNCTION',
    'READ',
    'WRITE',
    'IF',
    'ELSE',
    'ENDIF',
    'WHILE',
    'ENDWHILE',
    'CONTINUE',
    'BREAK',
    'RETURN',
    'INT',
    'VOID',
    'STRING',
    'FLOAT'
]

#All the possible tokens
tokens = [
    'STRINGLITERAL',
    'FLOATLITERAL',
    'INTLITERAL',
    'OPERATOR',
    'IDENTIFIER',
    'KEYWORD',
    'PROGRAM',
    'BEGIN',
    'END',
    'FUNCTION',
    'READ',
    'WRITE',
    'IF',
    'ELSE',
    'ENDIF',
    'WHILE',
    'ENDWHILE',
    'CONTINUE',
    'BREAK',
    'RETURN',
    'INT',
    'FLOAT',
    'VOID',
    'STRING',
    'STRINGEQUALS',
    'SEMICOLON',
    'ASSIGNMENT',
    'BOOLEANOPS',
    'COMMA',
    'LEFTPAREN',
    'RIGHTPAREN',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE'
]

#Strings are a " followed by some number of non ", followed by a "
t_STRINGLITERAL = r'"[^"]*"'
#Possible operators are <=, >=, :=, +, -, *, /, =, !=, <, >, (, ), ;, ','
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_COMMA = r','
t_STRINGEQUALS = r':='
t_SEMICOLON = r';'
t_BOOLEANOPS = r'<=|>=|<|!=|>|='
t_LEFTPAREN = r'\('
t_RIGHTPAREN = r'\)'
#Floats are 0 or more numbers, a ., and 1 or more numbers
t_FLOATLITERAL = r'[0-9]*\.[0-9]+'
#Ints are 1 or more numbers
t_INTLITERAL = r'[0-9]+'

#Identifiers are variables and keywords.
#Variables are a letter followed by 0 or more letters and numbers
#Keywords are listed at the top
def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value in reserved:
        t.type = t.value #'KEYWORD'
    return t

#Comments are a -- followed by the rest of the line
def t_COMMENT(t):
    r'--.*'
    pass

#This will pass over any character that doesn't fit the other rules
#It is mainly used to skip over whitespace characters
def t_error(t):
    t.lexer.skip(1)
    pass

littleLexer = lex.lex()

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


globalSymbolTable = SymbolTable("GLOBAL", None)
currentScope = globalSymbolTable
currentScope.parent = currentScope
lastType = None
index = -1
currentBlock = 1
parameterList = SymbolTable("Params", None)
funcList = SymbolTable("Funcs", None)
blockList = SymbolTable("Block", None)
lastFunc = ""
lastBlock = ""

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','MULTIPLY','DIVIDE'),
)

# dictionary of names
names = { }

def p_statement_start(p):
    'statement : PROGRAM IDENTIFIER BEGIN pgm_body END'

def p_pgm_body(p):
    '''pgm_body : decl func_decl'''

# Variable Handlers
def p_decl(p):
    '''decl : string_decl decl
            | var_decl decl
            | empty'''

def p_string_decl(p):
    "string_decl : STRING IDENTIFIER STRINGEQUALS STRINGLITERAL SEMICOLON "
    var = Variable(p[2], "STRING")
    var.setValue(p[4])
    currentScope.addVariable(var)
    names[p[2]] = p[4]

def p_var_decl(p):
    "var_decl : var_type id_list SEMICOLON"

def p_var_type(p):
    '''var_type : INT
                | FLOAT'''
    global lastType
    lastType = p[1]

def p_any_type(p):
    '''any_type : var_type
                | VOID'''
    global lastType
    lastType = p[1]

def p_id_list(p):
    "id_list : IDENTIFIER id_tail"
    global index
    if len(p) > 1:
        var = Variable(p[1], lastType)
        if index == -1:
            currentScope.addVariable(var)
        else:
            currentScope.insertVar(var, index)
            index = -1

def p_id_tail(p):
    '''id_tail : COMMA IDENTIFIER id_tail
               | empty'''
    global index
    if len(p) > 2:
        if not currentScope.containsName(p[2]):
            if index == -1:
                index = currentScope.getLength()

            var = Variable(p[2], lastType)
            currentScope.insertVar(var, index)

# These are for id_lists that aren't in var declaration
def p_id_list2(p):
    "id_list2 : IDENTIFIER id_tail2"

def p_id_tail2(p):
    '''id_tail2 : COMMA IDENTIFIER id_tail2
                 | empty'''


# Function Parameter List
def p_param_decl_list(p):
    '''param_decl_list : param_decl param_decl_tail
                       | empty'''

def p_param_decl(p):
    '''param_decl : var_type IDENTIFIER'''

    var = Variable(p[2], lastType)
    parameterList.addVariable(var)


def p_param_decl_tail(p):
    '''param_decl_tail : COMMA param_decl param_decl_tail
                       | empty'''

# Function Handlers
def p_func_decl(p):
    '''func_decl : func_declaration func_decl
                 | empty'''

def p_func_declaration(p):
    '''func_declaration : FUNCTION any_type IDENTIFIER LEFTPAREN param_decl_list RIGHTPAREN BEGIN func_body END '''
    global currentScope, lastFunc
    currentScope = currentScope.getParent()
    funcScope = SymbolTable(p[3], currentScope)
    currentScope.insertChild(funcScope, lastFunc)
    if not lastBlock == "":
        lastFunc = lastBlock
    else:
        lastFunc = p[3]

    # currentScope = funcScope
    params = parameterList.getValues()

    if len(params) > 0:
        for p in params:
            funcScope.addVariable(p)
        parameterList.clear()

    if len(funcList.getValues()) > 0:
        for v in funcList.getValues():
            funcScope.addVariable(v)
        funcList.clear()


def p_func_body(p):
    '''func_body : decl_func_var stmt_list'''

def p_decl_func_var(p):
    '''decl_func_var : string_decl_func decl_func_var
                     | var_decl_func decl_func_var
                     | empty'''

def p_string_decl_func(p):
    "string_decl_func : STRING IDENTIFIER STRINGEQUALS STRINGLITERAL SEMICOLON "
    var = Variable(p[2], "STRING")
    var.setValue(p[4])
    funcList.addVariable(var)
    names[p[2]] = p[4]

def p_var_decl_func(p):
    "var_decl_func : var_type id_list_func SEMICOLON"

def p_id_list_func(p):
    "id_list_func : IDENTIFIER id_tail_func"
    global index
    if len(p) > 1:
        var = Variable(p[1], lastType)
        if index == -1:
            funcList.addVariable(var)
        else:
            funcList.insertVar(var, index)
            index = -1

def p_id_tail_func(p):
    '''id_tail_func : COMMA IDENTIFIER id_tail_func
               | empty'''
    global index
    if len(p) > 2:
        if index == -1:
            index = funcList.getLength()

        var = Variable(p[2], lastType)
        funcList.insertVar(var, index)

        # Statement List
def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
                 | empty '''

def p_stmt(p):
    '''stmt : base_stmt
            | if_stmt
            | while_stmt'''

def p_base_stmt(p):
    '''base_stmt : assign_stmt
                 | read_stmt
                 | write_stmt
                 | return_stmt'''

# Basic Statements            
def p_assign_stmt(p):
    '''assign_stmt : assign_expr SEMICOLON'''

def p_assign_expr(p):
    '''assign_expr : IDENTIFIER STRINGEQUALS expr'''

def p_read_stmt(p):
    '''read_stmt : READ LEFTPAREN id_list2 RIGHTPAREN SEMICOLON'''

def p_write_stmt(p):
    "write_stmt : WRITE LEFTPAREN id_list2 RIGHTPAREN SEMICOLON"

def p_return_stmt(p):
    "return_stmt : RETURN expr SEMICOLON"

# Expressions
def p_expr(p):
    "expr : expr_prefix factor"

def p_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop
                   | empty'''

def p_factor(p):
    '''factor : factor_prefix postfix_expr'''

def p_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop
                     | empty'''

def p_postfix_expr(p):
    '''postfix_expr : primary
                    | call_expr'''

def p_call_expr(p):
    "call_expr : IDENTIFIER LEFTPAREN expr_list RIGHTPAREN "

def p_expr_list(p):
    '''expr_list : expr expr_list_tail
                 | empty'''

def p_expr_list_tail(p):
    '''expr_list_tail : COMMA expr expr_list_tail
                      | empty'''

def p_primary(p):
    '''primary : LEFTPAREN expr RIGHTPAREN
               | IDENTIFIER
               | INTLITERAL
               | FLOATLITERAL'''

def p_addop(p):
    '''addop : PLUS
             | MINUS '''

def p_mulop(p):
    '''mulop : MULTIPLY
             | DIVIDE '''

# Complex Statements and Conditions
def p_if_stmt(p):
    "if_stmt : IF LEFTPAREN cond RIGHTPAREN decl_block_var stmt_list else_part ENDIF"
    global currentScope, currentBlock, lastBlock

    currentScope = currentScope.getParent()
    blockScope = SymbolTable("BLOCK " + str(currentBlock), currentScope)
    lastBlock = "BLOCK " + str(currentBlock)
    currentScope.addChild(blockScope)
    currentBlock += 1
    # currentScope = blockScope
    # currentBlock

    if len(blockList.getValues()) > 0:
        for var in blockList.getValues():
            blockScope.addVariable(var)
        blockList.clear()

def p_else_part(p):
    '''else_part : ELSE decl_block_var stmt_list
                 | empty'''
    global currentScope, currentBlock, lastBlock

    if len(p) > 2:
        currentScope = currentScope.getParent()
        blockScope = SymbolTable("BLOCK " + str(currentBlock), currentScope)
        lastBlock = "BLOCK " + str(currentBlock)
        currentScope.addChild(blockScope)
        currentBlock += 1
        # currentScope = blockScope

        if len(blockList.getValues()) > 0:
            for var in blockList.getValues():
                blockScope.addVariable(var)
            blockList.clear()


def p_cond(p):
    "cond : expr compop expr"

def p_compop(p):
    '''compop : BOOLEANOPS'''

# While Statements
def p_while_stmt(p):
    "while_stmt : WHILE LEFTPAREN cond RIGHTPAREN decl_block_var stmt_list ENDWHILE"
    global currentScope, currentBlock

    currentScope = currentScope.getParent()
    blockScope = SymbolTable("BLOCK " + str(currentBlock), currentScope)
    lastBlock = "BLOCK " + str(currentBlock)
    currentScope.addChild(blockScope)
    currentBlock += 1
    #currentScope = blockScope

    if len(blockList.getValues()) > 0:
        for var in blockList.getValues():
            blockScope.addVariable(var)
        blockList.clear()

#################### these are for block statements #########################

def p_decl_block_var(p):
    '''decl_block_var : string_decl_block decl_block_var
                     | var_decl_block decl_block_var
                     | empty'''

def p_string_decl_block(p):
    "string_decl_block : STRING IDENTIFIER STRINGEQUALS STRINGLITERAL SEMICOLON "
    var = Variable(p[2], "STRING")
    var.setValue(p[4])
    blockList.addVariable(var)
    names[p[2]] = p[4]

def p_var_decl_block(p):
    "var_decl_block : var_type id_list_block SEMICOLON"

def p_id_list_block(p):
    "id_list_block : IDENTIFIER id_tail_block"
    global index
    if len(p) > 1:
        var = Variable(p[1], lastType)
        if index == -1:
            blockList.addVariable(var)
        else:
            blockList.insertVar(var, index)
            index = -1

def p_id_tail_block(p):
    '''id_tail_block : COMMA IDENTIFIER id_tail_block
               | empty'''
    global index
    if len(p) > 2:
        if index == -1:
            index = blockList.getLength()

        var = Variable(p[2], lastType)
        blockList.insertVar(var, index)

#############################################################################

def p_empty(p):
    'empty : '

def p_error(p):
    global error
    error = True

sys.path.insert(0,"ply-3.8/")
import ply.yacc as yacc
yacc.yacc()

# Reads in the file and processes it
with open(sys.argv[1], "r") as myFile:
    data = myFile.read()
    yacc.parse(input=data, lexer=littleLexer)

if error:
    print("DECLARATION ERROR " + duplicate)
else:
    globalSymbolTable.printSymbolTable()
