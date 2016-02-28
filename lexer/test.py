# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"ply-3.8/")

if sys.version_info[0] >= 3:
    raw_input = input

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
    'KEYWORD'
]

#Strings are a " followed by some number of non ", followed by a "
t_STRINGLITERAL = r'"[^"]*"'
#Possible operators are <=, >=, :=, +, -, *, /, =, !=, <, >, (, ), ;, ','
t_OPERATOR = r'<=|>=|:=|\+|-|\*|/|=|!=|<|>|\(|\)|;|,'
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
        t.type = 'KEYWORD'
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


# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
