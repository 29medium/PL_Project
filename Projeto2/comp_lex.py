# comp_lex.py
#
# Comando -> Atribuir | Imprimir
#
# Declarar -> int id '=' num ';'
#           | int id ';'
#           | int id '[' num ']' ';'
#
# Imprimir -> print id ';'
#
# Atribuir -> id '=' Exp ';'
#
# Exp -> Exp '+' Termo
#      | Exp '-' Termo
#      | Termo
#
# Termo -> Termo '*' Fator
#        | Termo '/' Fator
#        | Termo '%' Fator
#        | Fator
#
# Fator -> (Exp)
#        | num
#        | id

import ply.lex as lex

tokens = ['id', 'num', 'int', 'print']
literals = ['+', '-', '*', '/', '%', '(', ')', '=', ';']
 
t_num = r'\-?\d+'
t_int = r'int'
t_print = r'print'
t_id = r'\w'
t_ignore = " \t\n"

def t_error(t):
    print("Caráter ilegal: ", t.value[0])
    t.lexer().skip(1)

lexer = lex.lex()
