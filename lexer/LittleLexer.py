#!/usr/local/bin/python2.7


import sys
import lex

error = False

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

#Create lexer
# lexer = lex.lex()

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
    names[p[2]] = p[4]

def p_var_decl(p):
    "var_decl : var_type id_list SEMICOLON"

def p_var_type(p):
    '''var_type : INT
                | FLOAT'''

def p_any_type(p):
    '''any_type : var_type
                | VOID'''

def p_id_list(p):
    "id_list : IDENTIFIER id_tail"

def p_id_tail(p):
    '''id_tail : COMMA IDENTIFIER id_tail
               | empty'''

# Function Parameter List
def p_param_decl_list(p):
    '''param_decl_list : param_decl param_decl_tail
                       | empty'''

def p_param_decl(p):
    '''param_decl : var_type IDENTIFIER'''

def p_param_decl_tail(p):
    '''param_decl_tail : COMMA param_decl param_decl_tail
                       | empty'''

# Function Handlers
def p_func_decl(p):
    '''func_decl : func_declaration func_decl
                 | empty'''

def p_func_declaration(p):                 
    '''func_declaration : FUNCTION any_type IDENTIFIER LEFTPAREN param_decl_list RIGHTPAREN BEGIN func_body END '''

def p_func_body(p):
    '''func_body : decl stmt_list'''

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
    '''read_stmt : READ LEFTPAREN id_list RIGHTPAREN SEMICOLON'''

def p_write_stmt(p):
    "write_stmt : WRITE LEFTPAREN id_list RIGHTPAREN SEMICOLON"

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
    "if_stmt : IF LEFTPAREN cond RIGHTPAREN decl stmt_list else_part ENDIF"

def p_else_part(p):
    '''else_part : ELSE decl stmt_list
                 | empty'''

def p_cond(p):
    "cond : expr compop expr"

def p_compop(p):
    '''compop : BOOLEANOPS'''

# While Statements
def p_while_stmt(p):
    "while_stmt : WHILE LEFTPAREN cond RIGHTPAREN decl stmt_list ENDWHILE"

def p_empty(p):
    'empty : '

# funcs leftover from calc.py
#
#def p_expression_binop(p):
#    '''expression : expression '+' expression
#                  | expression '-' expression
#                  | expression '*' expression
#                  | expression '/' expression'''
#    if p[2] == '+'  : p[0] = p[1] + p[3]
#    elif p[2] == '-': p[0] = p[1] - p[3]
#    elif p[2] == '*': p[0] = p[1] * p[3]
#    elif p[2] == '/': p[0] = p[1] / p[3]

#def p_expression_group(p):
#    "expression : '(' expression ')'"
#	
#    p[0] = p[2]

#def p_expression_name(p):
#    "expression : IDENTIFIER"
#    try:
#        p[0] = names[p[1]]
#    except LookupError:
#        print("Undefined name '%s'" % p[1])
#        p[0] = 0

def p_error(p):
    global error
    error = True
#    if p:
#        print("Syntax error at '%s'" % p.value)
#    else:
#         print("Syntax error at EOF")

sys.path.insert(0,"ply-3.8/")
import ply.yacc as yacc
yacc.yacc()

# Reads in the file and processes it
with open(sys.argv[1], "r") as myFile:
    data = myFile.read()
    yacc.parse(input=data, lexer=littleLexer)

#f = open('Micro', 'w')

if error:
    #f.write("Not accepted")
    print("Not accepted")
else:
    #f.write("Accepted")
    print("Accepted")

