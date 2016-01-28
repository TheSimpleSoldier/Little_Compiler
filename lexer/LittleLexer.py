import lex
import sys

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

tokens = [
    'STRINGLITERAL',
    'FLOATLITERAL',
    'INTLITERAL',
    'OPERATOR',
    'IDENTIFIER',
    'KEYWORD'
]

t_STRINGLITERAL = r'"[^"]*"'
t_OPERATOR = r'<=|>=|:=|\+|-|\*|/|=|!=|<|>|\(|\)|;|,'
t_FLOATLITERAL = r'[0-9]*\.[0-9]+'
t_INTLITERAL = r'[0-9]+'

def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value in reserved:
        t.type = 'KEYWORD'
    return t

def t_COMMENT(t):
    r'--.*'
    pass

def t_error(t):
    t.lexer.skip(1)
    pass

lexer = lex.lex()


with open(sys.argv[1], "r") as myFile:
    data = myFile.read()
    lexer.input(data)

for tok in lexer:
    print("Token Type: " + tok.type)
    print("Value: " + str(tok.value))
