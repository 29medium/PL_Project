# comp_yacc.py

import ply.yacc as yacc
from comp_lex import tokens

def p_Comando_declarar(p):
    "Comando : Declarar"

def p_Comando_imprimir(p):
    "Comando : Imprimir"

def p_Comando_atribuir(p):
    "Comando : Atribuir"

def p_Declarar_exp(p):
    "Declarar : int id '=' Exp ';'"

    add_var(p[2], 1, p.parser.var)

    fileOut.write("pushi " + str(p[4]) + "\n")

def p_Declarar_vazio(p):
    "Declarar : int id ';'"

    add_var(p[2], 1, p.parser.var)

    fileOut.write("pushi 0\n")

def p_Imprimir(p):
    "Imprimir : print id ';'"

    index = get_index(p[2], p.parser.var)

    if index != None:
        fileOut.write("pushg " + str(index) + "\n")
        fileOut.write("writei\n")

def p_Atribuir_exp(p):
    "Atribuir : id '=' Exp ';'"

    index = get_index(p[1], p.parser.var)

    if index != None:
        fileOut.write(f"store {index}\n")

def p_Exp_add(p):
    "Exp : Exp '+' Termo"
    p[0] = p[1] + p[3]
    p.parser.intbuffer.append("pushi " + str(p[1]) + "\n")
    p.parser.intbuffer.append("pushi " + str(p[3]) + "\n")
    p.parser.operationbuffer.append("add\n")

def p_Exp_sub(p):
    "Exp : Exp '-' Termo"
    p[0] = p[1] - p[3]
    fileOut.write("pushi " + str(p[1]) + "\n")
    fileOut.write("pushi " + str(p[3]) + "\n")
    fileOut.write("sub\n")

def p_Exp_termo(p):
    "Exp : Termo"
    p[0] = p[1]

def p_Termo_mult(p):
    "Termo : Termo '*' Fator"
    p[0] = p[1] * p[3]
    fileOut.write("pushi " + str(p[1]) + "\n")
    fileOut.write("pushi " + str(p[3]) + "\n")
    fileOut.write("mul\n")

def p_Termo_div(p):
    "Termo : Termo '/' Fator"
    if p[3] != 0:
        p[0] = p[1] / p[3]
        fileOut.write("pushi " + str(p[1]) + "\n")
        fileOut.write("pushi " + str(p[3]) + "\n")
        fileOut.write("div\n")
    else:
        print("Erro: Divisão por zero")


def p_Termo_mod(p):
    "Termo : Termo '%' Fator"
    if p[3] != 0:
        p[0] = p[1] % p[3]
        fileOut.write("pushi " + str(p[1]) + "\n")
        fileOut.write("pushi " + str(p[3]) + "\n")
        fileOut.write("mod\n")
    else:
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
        print("Variável " + p[1] + " não definida")

def p_error(p):
    print("Syntax Error in input: ", p)

# Programa

def add_var(id, num, var):
    if id not in var:
        var[id] = num

def get_index(id, var):
    if id in var.keys():
        index = 0
        for key in var.keys():
            if key == id:
                break
            else:
                index += var[key]
        return index
    return None

def flush(intbuffer, operationbuffer):
    for i in intbuffer:
        fileOut.write(i)
    
    for i in operationbuffer:
        fileOut.write(i)

r = 1
while r:
    inFilePath = input("Code File Path >> ")
    
    try:
        fileIn = open(inFilePath, "r")
        r = 0
    except (FileNotFoundError, NotADirectoryError):
        print("Wrong File Path\n")

r = 1
while r:
    outFilePath = input("Output File Path >> ")

    if outFilePath != inFilePath:
        fileOut = open(outFilePath, "w")
        r = 0
    else:
        print("Wrong File Path\n")

parser = yacc.yacc()

parser.var = dict()
parser.intbuffer = list()
parser.operationbuffer = list()

fileOut.write("start\n")

for linha in fileIn:
    parser.parse(linha)

fileOut.write("stop\n")

fileIn.close()
fileOut.close()
