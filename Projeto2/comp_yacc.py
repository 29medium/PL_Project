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
    "TypeDeclarations : DECLARATIONS Declarations END"

    p[0] = p[2]

def p_Type_instructions(p):
    "TypeInstructions : INSTRUCTIONS Instructions END"

    p[0] = p[2]

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

    add_var(p[2], 1, 1, p)

    p[0] = p[4]

def p_Declararation_simple(p):
    "Declaration : INT ID ';'"

    add_var(p[2], 1, 1, p)

    p[0] = "pushi 0\n"


def p_Declararation_array_num(p):
    "Declaration : INT ID '[' NUM ']' ';'"

    col = int(p[4])
    add_var(p[2], col, 1, p)

    p[0] = f"pushn {col}\n"


def p_Declararation_matrix_num(p):
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

def p_Read_id(p):
    "Instruction : INPUT ID ';'"

    res = get_index(p[2], p)

    (_, _, offset) = res
    p[0] = f"read\natoi\nstoreg {offset}\n"

def p_Read_array(p):
    "Instruction : INPUT ID '[' Exp ']' ';'"

    res = get_index(p[2], p)

    (_, _, offset) = res
    p[0] = f"pushgp\npushi {offset}\npadd\n{p[4]}read\natoi\nstoren\n"
    
def p_Read_matrix(p):
    "Instruction : INPUT ID '[' Exp ']' '[' Exp ']' ';'"

    res = get_index(p[2], p)

    (col, _, offset) = res
    p[0] = f"\npushgp\npushi {offset}\npadd\n{p[4]}pushi {col}\nmul\n{p[7]}add\nread\natoi\nstoren\n"


# -----------------------------------------------------------------
#                         PRINT
# -----------------------------------------------------------------

def p_Print_Exp(p):
    "Instruction : PRINT Exp ';'"

    p[0] = f"{p[2]}writei\n"


def p_Print_Log(p):
    "Instruction : PRINT Log ';'"

    p[0] = f"{p[2]}writei\n"

# -----------------------------------------------------------------
#                         ATTRIBUTE
# -----------------------------------------------------------------

def p_Attribure(p):
    "Instruction : ID ATTR Exp ';'"

    res = get_index(p[1], p)

    (_, _, offset) = res
    p[0] = f"{p[3]}storeg {offset}\n"


def p_Attribure_array(p):
    "Instruction : ID '[' Exp ']' ATTR Exp ';'"

    res = get_index(p[1], p)
    
    (_, _, offset) = res

    p[0] = f"pushgp\npushi {offset}\npadd\n{p[3]}{p[6]}storen\n"


def p_Attribure_matrix(p):
    "Instruction : ID '[' Exp ']' '[' Exp ']' ATTR Exp ';'"

    res = get_index(p[1], p)

    (col, _, offset) = res

    p[0] = f"pushgp\npushi {offset}\npadd\n{p[3]}pushi {col}\nmul\n{p[6]}add\n{p[9]}storen\n"

# -----------------------------------------------------------------
#                              IF
# -----------------------------------------------------------------

def p_Condition(p):
    "Instruction : IF Rel THEN Instructions Else"
    p[0] = f"{p[2]}jz else{p.parser.ifs}\n{p[4]}jump endif{p.parser.ifs}\n{p[6]}\nendif{p.parser.ifs}:\n"
    p.parser.ifs += 1

def p_Condition_simple(p):
    "Instruction : IF Rel THEN Instructions END"
    p[0] = f"{p[2]}jz endif{p.parser.ifs}\n{p[4]}\nendif{p.parser.ifs}:\n"
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
    p[0] = f"{p[1]}{p[3]}equal\npushi 1\nequal\n"


def p_Log_or(p):
    "Log : Log OR Rel"
    p[0] = f"{p[1]}{p[3]}equal\npushi 0\nequal\nnot\n"

def p_Log_not(p):
    "Log : NOT Log"
    p[0] = "{p[2]}not\n"

def p_Log_Rel(p):
    "Log : Rel"
    p[0] = p[1]

def p_Rel_eq(p):
    "Rel : Rel EQ LExp"
    p[0] = f"{p[1]}{p[3]}equal\n"


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
    res = get_index(p[1], p)

    (_, _, offset) = res
    p[0] = f"pushg {offset}\n"


def p_LFactor_array(p):
    "LFactor : ID '[' Exp ']'"

    res = get_index(p[1], p)

    (_, _, offset) = res
    p[0] = f"pushgp\npushi {offset}\npadd\n{p[3]}loadn\n"


def p_LFactor_matrix(p):
    "LFactor : ID '[' Exp ']' '[' Exp ']'"

    res = get_index(p[1], p)

    (col, _, offset) = res
    p[0] = f"pushgp\npushi {offset}\npadd\n{p[3]}pushi {col}\nmul\n{p[6]}add\nloadn\n"

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
    res = get_index(p[1], p)

    (_, _, offset) = res
    p[0] = f"pushg {offset}\n"

def p_Factor_array(p):
    "Factor : ID '[' Exp ']'"

    res = get_index(p[1], p)

    (_, _, offset) = res
    p[0] = f"pushgp\npushi {offset}\npadd\n{p[3]}loadn\n"

def p_Factor_matrix(p):
    "Factor : ID '[' Exp ']' '[' Exp ']'"

    res = get_index(p[1], p)

    (col, _, offset) = res
    p[0] = f"pushgp\npushi {offset}\npadd\n{p[3]}pushi {col}\nmul\n{p[6]}add\nloadn\n"
    

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
        try:
            fileOut = open(outFilePath, "w")
            r = 0
        except (FileNotFoundError, NotADirectoryError):
            print("Wrong File Path\n")
    else:
        print("Wrong File Path\n")

parser = yacc.yacc()

parser.var = dict() # x => (col, line, offset)
parser.offset = 0
parser.ifs = 0
parser.cycles = 0

data = fileIn.read()
parser.parse(data)

fileIn.close()
fileOut.close()
