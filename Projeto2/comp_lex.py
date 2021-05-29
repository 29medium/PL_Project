import ply.lex as lex

reserved = {
    'int' : 'INT',
    'print' : 'PRINT',
    'input' : 'INPUT',
    'then' : 'THEN',
    'end': 'END',
    'declarations': 'DECLARATIONS',
    'instructions': 'INSTRUCTIONS',
    'if' : 'IF',
    'else' : 'ELSE',
    'repeat' : 'REPEAT',
    'until' : 'UNTIL',
    'while' : 'WHILE',
    'call' : 'CALL',
    'for' : 'FOR',
    'do' : 'DO',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'def' : 'DEF',
    'main' : 'MAIN'
}

tokens = ['ID', 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'EQ', 'NE', 'G', 'GE', 'L', 'LE', 'LPAR', 'RPAR', 'LBRA', 'RBRA', 'SC', 'ATTR', 'NUM', 'STRING'] + list(reserved.values())

def t_LPAR(t):
    r'\('
    t.type = reserved.get(t.value, 'LPAR')
    return t

def t_RPAR(t):
    r'\)'
    t.type = reserved.get(t.value, 'RPAR')
    return t

def t_LBRA(t):
    r'\['
    t.type = reserved.get(t.value, 'LBRA')
    return t

def t_RBRA(t):
    r'\]'
    t.type = reserved.get(t.value, 'RBRA')
    return t

def t_SC(t):
    r';'
    t.type = reserved.get(t.value, 'SC')
    return t

def t_C(t):
    r','
    t.type = reserved.get(t.value, 'C')
    return t

def t_ID(t):
    r'[a-z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_GE(t):
    r'>='
    t.type = reserved.get(t.value, 'GE')
    return t

def t_G(t):
    r'>'
    t.type = reserved.get(t.value, 'G')
    return t

def t_LE(t):
    r'<='
    t.type = reserved.get(t.value, 'LE')
    return t

def t_L(t):
    r'<'
    t.type = reserved.get(t.value, 'L')
    return t

def t_EQ(t):
    r'=='
    t.type = reserved.get(t.value, 'EQ')
    return t

def t_NE(t):
    r'!='
    t.type = reserved.get(t.value, 'NE')
    return t

def t_PLUS(t):
    r'\+'
    t.type = reserved.get(t.value, 'PLUS')
    return t

def t_MINUS(t):
    r'\-'
    t.type = reserved.get(t.value, 'MINUS')
    return t

def t_MUL(t):
    r'\*'
    t.type = reserved.get(t.value, 'MUL')
    return t

def t_DIV(t):
    r'/'
    t.type = reserved.get(t.value, 'DIV')
    return t

def t_MOD(t):
    r'%'
    t.type = reserved.get(t.value, 'MOD')
    return t

def t_ATTR(t):
    r'='
    t.type = reserved.get(t.value, 'ATTR')
    return t

def t_NUM(t):
    r'\-?\d+'
    t.type = reserved.get(t.value, 'NUM')
    return t

def t_STRING(t):
    r'\"[^"]+\"'
    t.type = reserved.get(t.value, 'STRING')
    return t

t_ignore = " \r\t\n"

def t_error(t):
    print("Illegal character: ", t.value[0])
    t.lexer().skip(1)

lexer = lex.lex()
