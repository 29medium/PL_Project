# comp_yacc.py

import ply.yacc as yacc
from comp_lex import tokens

# -----------------------------------------------------------------
#                              TYPE
# -----------------------------------------------------------------

def p_Type(p):
    "Type : TypeDeclarations TypeInstructions"

    fileOut.write(f"{p[1]}start\n{p[2]}stop\n")

def p_Type_declarations(p):
    "TypeDeclarations : DECLARATIONS BEGIN Declarations END"

    p[0] = p[3]

def p_Type_instructions(p):
    "TypeInstructions : INSTRUCTIONS BEGIN Instructions END"

    p[0] = p[3]

# -----------------------------------------------------------------
#                         DECLARATIONS
# -----------------------------------------------------------------

def p_Declarations(p):    
    "Declarations : Declarations Declaration"

    p[0] = p[1] + p[2]

def p_Declarations_empty(p):
    "Declarations : "

    p[0] = ""

def p_Declararation_exp(p):
    "Declaration : INT ID '=' Exp ';'"

    add_var(p[2], 1, p)

    p[0] = p[4]

def p_Declararation_simple(p):
    "Declaration : INT ID ';'"

    add_var(p[2], 1, p)

    p[0] = "pushi 0\n"


def p_Declararation_array(p):
    "Declaration : INT ID '[' NUM ']' ';'"

    add_var(p[2], int(p[4]), p)

    p[0] = f"pushn {p[4]}\n"

# -----------------------------------------------------------------
#                         INSTRUCTIONS
# -----------------------------------------------------------------

def p_Instructions(p):
    "Instructions : Instructions Instruction"

    p[0] = p[1] + p[2]

def p_Instructions_empty(p):
    "Instructions : "

    p[0] = ""

# -----------------------------------------------------------------
#                           INPUT
# -----------------------------------------------------------------

def p_Read(p):
    "Instruction : INPUT ID ';'"

    (size, offset) = get_index(p[2], p)

    if size == 1:
        p[0] = f"read\natoi\nstoreg {offset}\n"


def p_Print_array(p):
    "Instruction : INPUT ID '[' NUM ']' ';'"
    (size, offset) = get_index(p[2], p)

    if int(p[4]) < size and int(p[4]) >= 0:
        index = offset + int(p[4])
        p[0] = f"read\natoi\nstoreg {index}\n"
    
# -----------------------------------------------------------------
#                         PRINT
# -----------------------------------------------------------------

def p_Print(p):
    "Instruction : PRINT ID ';'"

    (size,offset) = get_index(p[2], p)

    if size == 1:
        p[0] = f"pushg {offset}\nwritei\n"
    else:
        p[0] = ""
        for i in range(offset,offset + size):
            p[0] += f"pushg {i}\nwritei\n"

def p_Print_array(p):
    "Instruction : PRINT ID '[' NUM ']' ';'"
    (size, offset) = get_index(p[2], p)

    if int(p[4]) < size and int(p[4]) >= 0:
        index = offset + int(p[4])
        p[0] = f"pushg {index}\nwritei\n"

# -----------------------------------------------------------------
#                         ATTRIBUTE
# -----------------------------------------------------------------

def p_Attribure(p):
    "Instruction : ID '=' Exp ';'"

    (size,offset) = get_index(p[1], p)

    if size == 1:
        p[0] = f"{p[3]}storeg {offset}\n"

def p_Attribure_array(p):
    "Instruction : ID '[' NUM ']' '=' Exp ';'"

    (size, offset) = get_index(p[1], p)

    if int(p[3]) < size and int(p[3]) >= 0:
        index = offset + int(p[3])
        p[0] = f"{p[6]}storeg {index}\n"

# -----------------------------------------------------------------
#                              IF
# -----------------------------------------------------------------

# -----------------------------------------------------------------
#                           REPEAT
# -----------------------------------------------------------------

# -----------------------------------------------------------------
#                       EXP TERM FACTOR
# -----------------------------------------------------------------

def p_Exp_add(p):
    "Exp : Exp '+' Term"
    p[0] = p[1] + p[3] + "add\n"

def p_Exp_sub(p):
    "Exp : Exp '-' Term"
    p[0] = p[1] + p[3] + "sub\n"

def p_Exp_term(p):
    "Exp : Term"
    p[0] = p[1]

def p_Term_mult(p):
    "Term : Term '*' Factor"
    p[0] = p[1] + p[3] + "mul\n"

def p_Term_div(p):
    "Term : Term '/' Factor"
    if p[3] != 0:
        p[0] = p[1] + p[3] + "div\n"
    else:
        p[0] = p[1] + "pushi 1\ndiv\n"

def p_Term_mod(p):
    "Term : Term '%' Factor"
    if p[3] != 0:
        p[0] = p[1] + p[3] + "mod\n"
    else:
        p[0] = p[1] + "pushi 1\nmod\n"

def p_Termo_fator(p):
    "Term : Factor"
    p[0] = p[1]

def p_Factor_par(p):
    "Factor : '(' Exp ')'"
    p[0] = p[2]

def p_Factor_num(p):
    "Factor : NUM"
    p[0] = f"pushi {p[1]}\n"

def p_Factor_id(p):
    "Factor : ID"
    (_, offset) = get_index(p[1], p)
    p[0] = f"pushg {offset}\n"

def p_Factor_id_array(p):
    "Factor : ID '[' NUM ']'"
    (size, offset) = get_index(p[1], p)

    if int(p[2]) < size and int(p[3]) >=0:
        index = offset+p[3]
        p[0] = f"pushg {index}\n"


# -----------------------------------------------------------------
#                         OTHER
# -----------------------------------------------------------------

def p_error(p):
    print("Syntax Error in input: ", p)

def add_var(id, size, p):
    if id not in p.parser.var.keys():
        p.parser.var[id] = (size, p.parser.offset)
        p.parser.offset += size

def get_index(id, p):
    if id in p.parser.var.keys():
        return p.parser.var[id]

# -----------------------------------------------------------------
#                         RUN
# -----------------------------------------------------------------

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

parser.var = dict() # x => (size, offset)
parser.offset = 0

for linha in fileIn:
    parser.parse(linha)

fileIn.close()
fileOut.close()
