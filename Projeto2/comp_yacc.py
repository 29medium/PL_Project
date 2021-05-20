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
    "Declaration : INT ID ATTR Exp ';'"

    add_var(p[2], 1, p)

    p[0] = p[4]

def p_Declararation_simple(p):
    "Declaration : INT ID ';'"

    add_var(p[2], 1, 1, p)

    p[0] = "pushi 0\n"


def p_Declararation_array(p):
    "Declaration : INT ID '[' NUM ']' ';'"

    add_var(p[2], int(p[4]), 1, p)

    p[0] = f"pushn {p[4]}\n"


def p_Declararation_matrix(p):
    "Declaration : INT ID '[' NUM ']' '[' NUM ']' ';'"

    add_var(p[2], int(p[7]), int(p[4]), p)

    size = int(p[7]) * int(p[4])
    p[0] = f"pushn {size}\n"

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

def p_Read_num(p):
    "Instruction : INPUT ID ';'"

    res = get_index(p[2], p)

    if res:
        (col, line, offset) = res
        if col == 1 and line == 1 and res:
            p[0] = f"read\natoi\nstoreg {offset}\n"
        else:
            p[0] = ""
    else:
        p[0] = ""

def p_Read_array(p):
    "Instruction : INPUT ID '[' NUM ']' ';'"

    res = get_index(p[2], p)

    if res:
        (col, line, offset) = res
        if col > int(p[4]) and int(p[4]) >= 0 and line == 1:
            offset = offset + int(p[4])
            p[0] = f"read\natoi\nstoreg {offset}\n"
        else:
            p[0] = ""
    else:
        p[0] = ""
    
def p_Read_matrix(p):
    "Instruction : INPUT ID '[' NUM ']' '[' NUM ']' ';'"

    res = get_index(p[2], p)

    if res:
        (col, line, offset) = res
        if col > int(p[7]) and int(p[7]) >= 0 and line > int(p[4]) and int(p[4]) >= 0:
            offset = offset + int(p[4])*col + int(p[7])
            p[0] = f"read\natoi\nstoreg {offset}\n"
        else:
            p[0] = ""
    else:
        p[0] = ""

# -----------------------------------------------------------------
#                         PRINT
# -----------------------------------------------------------------

def p_Print_num(p):
    "Instruction : PRINT ID ';'"

    res = get_index(p[2], p)

    if res:
        (col, line, offset) = res
        if col == 1 and line == 1 and res:
            p[0] = f"pushg {offset}\nwritei\n"
        else:
            p[0] = ""
    else:
        p[0] = ""

def p_Print_array(p):
    "Instruction : PRINT ID '[' NUM ']' ';'"

    res = get_index(p[2], p)

    if res:
        (col, line, offset) = res
        if col > int(p[4]) and int(p[4]) >= 0 and line == 1:
            offset = offset + int(p[4])
            p[0] = f"pushg {offset}\nwritei\n"
        else:
            p[0] = ""
    else:
        p[0] = ""


def p_Print_matrix(p):
    "Instruction : PRINT ID '[' NUM ']' '[' NUM ']' ';'"

    res = get_index(p[2], p)

    if res:
        (col, line, offset) = res
        if col > int(p[7]) and int(p[7]) >= 0 and line > int(p[4]) and int(p[4]) >= 0:
            offset = offset + int(p[4])*col + int(p[7])
            p[0] = f"pushg {offset}\nwritei\n"
        else:
            p[0] = ""
    else:
        p[0] = ""

# -----------------------------------------------------------------
#                         ATTRIBUTE
# -----------------------------------------------------------------

def p_Attribure(p):
    "Instruction : ID ATTR Exp ';'"

    res = get_index(p[1], p)

    if res:
        (col, line, offset) = res
        if col == 1 and line == 1 and res:
            p[0] = f"{p[3]}storeg {offset}\n"
        else:
            p[0] = ""
    else:
        p[0] = ""

def p_Attribure_array(p):
    "Instruction : ID '[' NUM ']' ATTR Exp ';'"

    res = get_index(p[1], p)

    if res:
        (col, line, offset) = res
        if col > int(p[3]) and int(p[3]) >= 0 and line == 1:
            offset = offset + int(p[3])
            p[0] = f"{p[6]}storeg {offset}\n"
        else:
            p[0] = ""
    else:
        p[0] = ""


def p_Attribure_matrix(p):
    "Instruction : ID '[' NUM ']' '[' NUM ']' ATTR Exp ';'"

    res = get_index(p[1], p)

    if res:
        (col, line, offset) = res
        if col > int(p[6]) and int(p[6]) >= 0 and line > int(p[3]) and int(p[3]) >= 0:
            offset = offset + int(p[3])*col + int(p[6])
            p[0] = f"{p[9]}storeg {offset}\n"
        else:
            p[0] = ""
    else:
        p[0] = ""

# -----------------------------------------------------------------
#                              IF
# -----------------------------------------------------------------

def p_Condition(p):
    "Instruction : IF Rel THEN Instructions Else"
    p[0] = f"{p[2]}jz else{p.parser.ifs}\n{p[4]}jump endif{p.parser.ifs}\n{p[6]}\nendif{p.parser.ifs}:\n"
    p.parser.ifs += 1

def p_Condition_simple(p):
    "Instruction : IF Rel THEN Instructions END"
    p[0] = f"{p[2]}jump end_if{p.parser.ifs}\n{p[4]}\nendif{p.parser.ifs}:\n"
    p.parser.ifs += 1

def p_Condition_Else(p):
    "Else : ELSE Instructions END"
    p[0] = f"\nelse{p.parser.ifs}:\n{p[2]}"

# -----------------------------------------------------------------
#                           REPEAT
# -----------------------------------------------------------------

def p_Cycle(p):
    "Instruction : REPEAT Instructions UNTIL Rel END"
    p[0] = f"cycle{p.parser.cycles}:\n{p[2]}{p[4]}jz cycle{p.parser.cycles}\n"
    p.parser.cycles += 1

# -----------------------------------------------------------------
#                 LOGIC AND RELATIONAL OPERATIONS
# -----------------------------------------------------------------

def p_Log_and(p):
    "Log : Log AND Rel"
    p[0] = p[1] + p[3] + "and\n"


def p_Log_or(p):
    "Log : Log OR Rel"
    p[0] = p[1] + p[3] + "or\n"

def p_Log_not(p):
    "Log : NOT Log"
    p[0] = p[2] + "not\n" 

def p_Log_Rel(p):
    "Log : Rel"
    p[0] = p[1]

def p_Rel_eq(p):
    "Rel : Rel EQ LExp"
    p[0] = p[1] + p[3] + "equal\n"


def p_Rel_ne(p):
    "Rel : Rel NE LExp"
    p[0] = p[1] + p[3] + "equal\n" + "not\n"


def p_Rel_g(p):
    "Rel : Rel G LExp"
    p[0] = p[1] + p[3] + "sup\n"


def p_Rel_ge(p):
    "Rel : Rel GE LExp"
    p[0] = p[1] + p[3] + "supeq\n"


def p_Rel_l(p):
    "Rel : Rel L LExp"
    p[0] = p[1] + p[3] + "inf\n"


def p_LTerm_le(p):
    "Rel : Rel LE LExp"
    p[0] = p[1] + p[3] + "infeq\n"


def p_Rel_exp(p):
    "Rel : LExp"
    p[0] = p[1]


def p_LExp_add(p):
    "LExp : LExp PLUS LTerm"
    p[0] = p[1] + p[3] + "add\n"


def p_LExp_sub(p):
    "LExp : LExp MINUS LTerm"
    p[0] = p[1] + p[3] + "sub\n"


def p_LExp_term(p):
    "LExp : LTerm"
    p[0] = p[1]


def p_LTerm_mult(p):
    "LTerm : LTerm MUL LFactor"
    p[0] = p[1] + p[3] + "mul\n"


def p_LTerm_div(p):
    "LTerm : LTerm DIV LFactor"
    if p[3] != 0:
        p[0] = p[1] + p[3] + "div\n"
    else:
        p[0] = p[1] + "pushi 1\ndiv\n"


def p_LTerm_mod(p):
    "LTerm : LTerm MOD LFactor"
    if p[3] != 0:
        p[0] = p[1] + p[3] + "mod\n"
    else:
        p[0] = p[1] + "pushi 1\nmod\n"


def p_LTerm_factor(p):
    "LTerm : LFactor"
    p[0] = p[1]


def p_LFactor_par(p):
    "LFactor : '(' Log ')'"
    p[0] = p[2]


def p_LFactor_num(p):
    "LFactor : NUM"
    p[0] = f"pushi {p[1]}\n"


def p_LFactor_id(p):
    "LFactor : ID"
    (_, offset) = get_index(p[1], p)
    p[0] = f"pushg {offset}\n"


def p_LFactor_id_array(p):
    "LFactor : ID '[' NUM ']'"
    (size, offset) = get_index(p[1], p)

    if int(p[2]) < size and int(p[3]) >= 0:
        index = offset+p[3]
        p[0] = f"pushg {index}\n"

# -----------------------------------------------------------------
#                    ARITHMETIC OPERATIONS
# -----------------------------------------------------------------

def p_Exp_add(p):
    "Exp : Exp PLUS Term"
    p[0] = p[1] + p[3] + "add\n"

def p_Exp_sub(p):
    "Exp : Exp MINUS Term"
    p[0] = p[1] + p[3] + "sub\n"

def p_Exp_term(p):
    "Exp : Term"
    p[0] = p[1]

def p_Term_mult(p):
    "Term : Term MUL Factor"
    p[0] = p[1] + p[3] + "mul\n"

def p_Term_div(p):
    "Term : Term DIV Factor"
    if p[3] != 0:
        p[0] = p[1] + p[3] + "div\n"
    else:
        p[0] = p[1] + "pushi 1\ndiv\n"

def p_Term_mod(p):
    "Term : Term MOD Factor"
    if p[3] != 0:
        p[0] = p[1] + p[3] + "mod\n"
    else:
        p[0] = p[1] + "pushi 1\nmod\n"

def p_Term_factor(p):
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

def add_var(id, col, line, p):
    if id not in p.parser.var.keys():
        p.parser.var[id] = (col, line, p.parser.offset)
        p.parser.offset += col * line

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

parser.var = dict() # x => (col, line, offset)
parser.offset = 0
parser.ifs = 0
parser.cycles = 0

for linha in fileIn:
    parser.parse(linha)

fileIn.close()
fileOut.close()
