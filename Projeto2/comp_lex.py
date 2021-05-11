# comp_lex.py
#
# Comando -> Atribuir
#
# Atribuir -> id = num
#           | id = id
#
# Exp -> Exp '+' Termo
#      | Exp '-' Termo
#      | Termo
#
# Termo -> Termo '*' Fator
#        | Termo '/' Fator
#        | Fator
#
# Fator -> (Exp)
#        | num
#        | id

import ply.lex as lex

tokens = ['id', 'num']
literals = ['+', '-', '*', '/', '(', ')', '=']

t_num = r'[+\-]?\d+'
t_id = r'[a-z]'
t_ignore = " \t\n"

def t_error(t):
    print("Caráter ilegal: ", t.value[0])
    t.lexer().skip(1)

lexer = lex.lex()
