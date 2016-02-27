import lex

import ply.yacc as yacc

def parser(lexer):
	yacc.yacc()
	for tok in lexer:
		print("Token Type: " + tok.type)
		print("Value: " + str(tok.value))
		yacc.parse(tok)
