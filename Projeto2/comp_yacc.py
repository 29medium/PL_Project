# comp_yacc.py

import ply.yacc as yacc
from comp_lex import tokens
import os

# -----------------------------------------------------------------
#                           Program
# -----------------------------------------------------------------

def p_Program(p):
    "Program : Main Functions"
    p[0] = p[1] + p[2]

# -----------------------------------------------------------------
#                           MAIN
# -----------------------------------------------------------------

def p_Main(p):
    "Main : DEF MAIN MainDeclarations MainInstructions END"

    p[0] = f"{p[3]}start\n{p[4]}stop\n"

def p_Main_declarations(p):
    "MainDeclarations : DECLARATIONS Declarations END"

    p[0] = p[2]

def p_Main_instructions(p):
    "MainInstructions : INSTRUCTIONS Instructions END"

    p[0] = p[2]

# -----------------------------------------------------------------
#                         Functions
# -----------------------------------------------------------------

def p_Functions(p):
    "Functions : Functions Function"
    p[0] = p[1] + p[2]

def p_Functions_empty(p):
    "Functions : "
    p[0] = ""

def p_Function(p):
    "Function : DEF ID Instructions END"

    add_func(p[2], p)

    p[0] = f"{p[2]}:\n{p[3]}return\n"

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
    "Declaration : INT ID ATTR Exp SC"

    add_var(p[2], 1, 1, p)

    p[0] = p[4]

def p_Declararation_simple(p):
    "Declaration : INT ID SC"

    add_var(p[2], 1, 1, p)

    p[0] = "pushi 0\n"


def p_Declararation_array_num(p):
    "Declaration : INT ID LBRA NUM RBRA SC"

    col = int(p[4])
    add_var(p[2], col, 1, p)

    p[0] = f"pushn {col}\n"


def p_Declararation_matrix_num(p):
    "Declaration : INT ID LBRA NUM RBRA LBRA NUM RBRA SC"

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
#                        CALL FUNCTION
# -----------------------------------------------------------------

def p_Call(p):
    "Instruction : CALL ID SC"

    add_func_called(p[2], p)

    p[0] = f"pusha {p[2]}\ncall\n"

# -----------------------------------------------------------------
#                           INPUT
# -----------------------------------------------------------------

def p_Read_id(p):
    "Instruction : INPUT ID SC"

    res = get_index(p[2], p)

    (_, _, offset) = res
    p[0] = f'''pushs ">> "\nwrites\nread\natoi\nstoreg {offset}\n'''

def p_Read_array(p):
    "Instruction : INPUT ID LBRA Exp RBRA SC"

    res = get_index(p[2], p)

    (_, _, offset) = res
    p[0] = f'''pushs ">> "\nwrites\npushgp\npushi {offset}\npadd\n{p[4]}read\natoi\nstoren\n'''

def p_Read_matrix(p):
    "Instruction : INPUT ID LBRA Exp RBRA LBRA Exp RBRA SC"

    res = get_index(p[2], p)

    (col, _, offset) = res
    p[0] = f'''pushs ">> "\nwrites\npushgp\npushi {offset}\npadd\n{p[4]}pushi {col}\nmul\n{p[7]}add\nread\natoi\nstoren\n'''


# -----------------------------------------------------------------
#                         PRINT
# -----------------------------------------------------------------

def p_Print(p):
    "Instruction : PRINT Line SC"
    p[0] = p[2]

def p_Line_String(p):
    "Line : STRING"

    p[0] = f'''pushs {p[1]}\nwrites\npushs "\\n"\nwrites\n'''

def p_Line_Log(p):
    "Line : Log"

    p[0] = f'''{p[1]}writei\npushs "\\n"\nwrites\n'''

# -----------------------------------------------------------------
#                         ATTRIBUTE
# -----------------------------------------------------------------

def p_Attribure(p):
    "Instruction : ID ATTR Exp SC"

    res = get_index(p[1], p)

    (_, _, offset) = res
    p[0] = f"{p[3]}storeg {offset}\n"

def p_Attribure_array(p):
    "Instruction : ID LBRA Exp RBRA ATTR Exp SC"

    res = get_index(p[1], p)

    (_, _, offset) = res

    p[0] = f"pushgp\npushi {offset}\npadd\n{p[3]}{p[6]}storen\n"

def p_Attribure_matrix(p):
    "Instruction : ID LBRA Exp RBRA LBRA Exp RBRA ATTR Exp SC"

    res = get_index(p[1], p)

    (col, _, offset) = res

    p[0] = f"pushgp\npushi {offset}\npadd\n{p[3]}pushi {col}\nmul\n{p[6]}add\n{p[9]}storen\n"
# -----------------------------------------------------------------
#                              IF
# -----------------------------------------------------------------

def p_Condition(p):
    "Instruction : IF LPAR Log RPAR THEN Instructions ELSE Instructions END"
    p[0] = f"{p[3]}jz else{p.parser.ifs}\n{p[6]}jump endif{p.parser.ifs}\nelse{p.parser.ifs}:\n{p[8]}\nendif{p.parser.ifs}:\n"
    p.parser.ifs += 1

def p_Condition_simple(p):
    "Instruction : IF LPAR Log RPAR THEN Instructions END"
    p[0] = f"{p[3]}jz endif{p.parser.ifs}\n{p[6]}\nendif{p.parser.ifs}:\n"
    p.parser.ifs += 1

# -----------------------------------------------------------------
#                           CYCLE
# -----------------------------------------------------------------

def p_Cycle_Repeat_Until(p):
    "Instruction : REPEAT Instructions UNTIL LPAR Log RPAR END"
    p[0] = f"cycle{p.parser.cycles}:\n{p[2]}{p[5]}jz cycle{p.parser.cycles}\n"
    p.parser.cycles += 1

def p_Cycle_While_Do(p):
    "Instruction : WHILE LPAR Log RPAR DO Instructions END"
    p[0] = f"cycle{p.parser.cycles}:\n{p[3]}jz endcycle{p.parser.cycles}\n{p[6]}jump cycle{p.parser.cycles}\nendcycle{p.parser.cycles}:\n"
    p.parser.cycles += 1

def p_Cycle_For_Do(p):
    "Instruction : FOR LPAR ID ATTR Exp SC Log SC ID ATTR Exp RPAR DO Instructions END"

    res1 = get_index(p[3], p)
    (_, _, offset1) = res1

    res2 = get_index(p[9], p)
    (_, _, offset2) = res2

    p[0] = f"{p[5]}storeg {offset1}\ncycle{p.parser.cycles}:\n{p[7]}jz endcycle{p.parser.cycles}\n{p[14]}{p[11]}storeg {offset2}\njump cycle{p.parser.cycles}\nendcycle{p.parser.cycles}:\n"
    p.parser.cycles += 1

# -----------------------------------------------------------------
#                         OPERATIONS
# -----------------------------------------------------------------

def p_Log_and(p):
    "Log : Log AND Rel"
    p[0] = f"{p[1]}{p[3]}mul\n"

def p_Log_or(p):
    "Log : Log OR Rel"
    p[0] = f"{p[1]}{p[3]}add\n{p[1]}{p[3]}mul\nsub\n"

def p_Log_not(p):
    "Log : NOT Rel"
    p[0] = "{p[2]}not\n"

def p_Log_Rel(p):
    "Log : Rel"
    p[0] = p[1]

def p_Rel_g(p):
    "Rel : Rel G Rel2"
    p[0] = f"{p[1]}{p[3]}sup\n"

def p_Rel_ge(p):
    "Rel : Rel GE Rel2"
    p[0] = f"{p[1]}{p[3]}supeq\n"

def p_Rel_l(p):
    "Rel : Rel L Rel2"
    p[0] = f"{p[1]}{p[3]}inf\n"

def p_Rel_le(p):
    "Rel : Rel LE Rel2"
    p[0] = f"{p[1]}{p[3]}infeq\n"

def p_Rel_rel2(p):
    "Rel : Rel2"
    p[0] = p[1]

def p_Rel2_eq(p):
    "Rel2 : Rel2 EQ Exp"
    p[0] = f"{p[1]}{p[3]}equal\n"

def p_Rel2_ne(p):
    "Rel2 : Rel2 NE Exp"
    p[0] = f"{p[1]}{p[3]}equal\nnot\n"

def p_Rel2_lexp(p):
    "Rel2 : Exp"
    p[0] = p[1]

def p_Exp_add(p):
    "Exp : Exp PLUS Term"
    p[0] = f"{p[1]}{p[3]}add\n"

def p_Exp_sub(p):
    "Exp : Exp MINUS Term"
    p[0] = f"{p[1]}{p[3]}sub\n"

def p_Exp_term(p):
    "Exp : Term"
    p[0] = p[1]

def p_Term_mult(p):
    "Term : Term MUL Factor"
    p[0] = f"{p[1]}{p[3]}mul\n"

def p_Term_div(p):
    "Term : Term DIV Factor"
    p[0] = f"{p[1]}{p[3]}div\n"

def p_Term_mod(p):
    "Term : Term MOD Factor"
    p[0] = f"{p[1]}{p[3]}mod\n"

def p_Term_factor(p):
    "Term : Factor"
    p[0] = p[1]

def p_Factor_par(p):
    "Factor : LPAR Log RPAR"
    p[0] = p[2]

def p_Factor_num(p):
    "Factor : NUM"
    p[0] = f"pushi {p[1]}\n"

def p_Factor_id(p):
    "Factor : ID"
    res = get_index(p[1], p)

    (_, _, offset) = res
    p[0] = f"pushg {offset}\n"

def p_Factor_array(p):
    "Factor : ID LBRA Exp RBRA"

    res = get_index(p[1], p)

    (_, _, offset) = res
    p[0] = f"pushgp\npushi {offset}\npadd\n{p[3]}loadn\n"

def p_Factor_matrix(p):
    "Factor : ID LBRA Exp RBRA LBRA Exp RBRA"

    res = get_index(p[1], p)

    (col, _, offset) = res
    p[0] = f"pushgp\npushi {offset}\npadd\n{p[3]}pushi {col}\nmul\n{p[6]}add\nloadn\n"

# -----------------------------------------------------------------
#                         OTHER
# -----------------------------------------------------------------

def p_error(p):
    print("\nCompilation error, aborting!")

def add_var(id, col, line, p):
    if id not in p.parser.var.keys():
        p.parser.var[id] = (col, line, p.parser.offset)
        p.parser.offset += col * line
    else:
        raise Exception

def get_index(id, p):
    if id in p.parser.var.keys():
        return p.parser.var[id]
    
def add_func(name, p):
    if name not in p.parser.funcs:
        p.parser.funcs.add(name)
    else:
        raise Exception

def add_func_called(name, p):
    if name not in p.parser.called_funcs:
        p.parser.called_funcs.add(name)

def check_called_funcs(parser):
    for called in parser.called_funcs:
        if called not in parser.funcs:
            raise Exception

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
        try:
            fileOut = open(outFilePath, "w")
            r = 0
        except (FileNotFoundError, NotADirectoryError):
            print("Wrong File Path\n")
    else:
        print("Wrong File Path\n")

parser = yacc.yacc()

parser.var = dict() # x => (col, line, offset)
parser.funcs = set()
parser.called_funcs = set()
parser.offset = 0
parser.ifs = 0
parser.cycles = 0

data = fileIn.read()

try:
    result = parser.parse(data)
    fileOut.write(result)
    check_called_funcs(parser)
except (TypeError, Exception):
    print("\nCompilation error, aborting!")
    os.remove(outFilePath)

fileIn.close()
fileOut.close()
