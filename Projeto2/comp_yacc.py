# comp_yacc.py

import ply.yacc as yacc
from comp_lex import tokens

# DECLARATIONS

def p_Type_declaration(p):
    "Type : DECLARATIONS Declarations END"

def p_Declarations(p):
    "Declarations : Declarations Declaration"

def p_Declarations_simple(p):
    "Declarations : Declaration"

def p_Declarations_empty(p):
    "Declarations : "

def p_Declararation_exp(p):
    "Declaration : INT ID '=' Exp ';'"

    add_var(p[2], 1, p.parser.var)

    fileOut.write("pushi " + str(p[4]) + "\n")

def p_Declararation_simple(p):
    "Declaration : INT ID ';'"

    add_var(p[2], 1, p.parser.var)

    fileOut.write("pushi 0\n")

# INSTRUCTIONS

def p_Type_instruction(p):
   "Type : INSTRUCTIONS Instructions END"

def p_Instructions(p):
    "Instructions : Instructions Instruction"

def p_Instructions_simple(p):
    "Instructions : Instruction"

def p_Instructions_empty(p):
    "Instructions : "

def p_Imprimir(p):
    "Instruction : PRINT ID ';'"

    index = get_index(p[2], p.parser.var)

    if index != None:
        fileOut.write("pushg " + str(index) + "\n")
        fileOut.write("writei\n")

def p_Atribuir_exp(p):
    "Instruction : ID '=' Exp ';'"

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

def p_Fator_par(p):
    "Fator : '(' Exp ')'"
    
def p_Fator_num(p):
    "Fator : NUM"
    # Passar o numero

def p_Fator_id(p):
    "Fator : ID"
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
