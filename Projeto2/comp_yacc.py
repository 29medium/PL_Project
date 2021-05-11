# comp_yacc.py
#

import ply.yacc as yacc
import sys

from comp_lex import tokens

def p_Comando_atribuir(p):
    "Comando : id '=' Exp"
    p.parser.vars[p[1]] = p[3]

def p_Comando_atribuir_vazio(p):
    "Comando : id"
    p.parser.vars[p[1]] = 0

def p_Exp_add(p):
    "Exp : Exp '+' Termo"
    p[0] = p[1] + p[3]

def p_Exp_sub(p):
    "Exp : Exp '-' Termo"
    p[0] = p[1] - p[3]

def p_Exp_termo(p):
    "Exp : Termo"
    p[0] = p[1]

def p_Termo_mult(p):
    "Termo : Termo '*' Fator"
    p[0] = p[1] * p[3]

def p_Termo_div(p):
    "Termo : Termo '/' Fator"
    if p[3] != 0:
        p[0] = p[1] / p[3]
    else:
        p.parser.success = False
        print("Erro: Divisão por zero")

def p_Termo_fator(p):
    "Termo : Fator"
    p[0] = p[1]

def p_Fator_par(p):
    "Fator : '(' Exp ')'"
    p[0] = p[2]

def p_Fator_num(p):
    "Fator : num"
    p[0] = int(p[1])

def p_Fator_id(p):
    "Fator : id"
    if p[1] in p.parser.vars:
        p[0] = p.parser.vars[p[1]]
    else:
        p.parser.success = False
        print("Variável " + p[1] + " não definida")

def p_error(p):
    p.parser.success = False
    print("Syntax Error in input: ", p)

parser = yacc.yacc()

parser.vars = dict()

for linha in sys.stdin:
    parser.success = True
    result = parser.parse(linha)
    if parser.success:
        print("Resultado: " + str(result))

print(parser.vars)