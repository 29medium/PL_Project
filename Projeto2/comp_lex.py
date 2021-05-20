# comp_lex.py
#
# Type -> Declaration | Instruction
#
# Declaration -> Declarationaux
#
# Declarationaux -> int id '=' num ';'
#                 | int id ';'
#                 | int id '[' num ']' ';'
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

reserved = {
    'int' : 'INT',
    'print' : 'PRINT',
    'input' : 'INPUT',
    'declarations': 'DECLARATIONS',
    'instructions': 'INSTRUCTIONS',
    'begin' : 'BEGIN',
    'end': 'END',
    'if' : 'IF',
    'elif' : 'ELSEIF',
    'else' : 'ELSE'
}

tokens = ['ID', 'NUM'] + list(reserved.values())
literals = ['+', '-', '*', '/', '%', '(', ')', '[', ']', '=', ';']

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_NUM(t):
    r'\-?\d+'
    t.type = reserved.get(t.value, 'NUM')
    return t

t_ignore = " \t\n"

def t_error(t):
    print("Illegal character: ", t.value[0])
    t.lexer().skip(1)

lexer = lex.lex()

# file = open('test','r')
# for line in file:
#     lexer.input(line)
#     tok = lexer.token()
#     while tok:
#         print(tok)
#         tok = lexer.token()
