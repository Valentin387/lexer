'''Detalles de la tarea
Analizador Léxico
Angel Augusto Agudelo Zapata
•
14:06
100 puntos
Fecha de entrega: 25 ago
Con base en el archivo adjunto, terminar el Analizador léxico para el lenguaje MiniC. Lo mas importante son las pruebas que realicen.

tokenizer.py
Texto
Comentarios de la clase
Tu trabajo
Asignado
Comentarios privados
'''
'''
tokenizer.py

El papel de este programa es convertir texto sin procesar en simbolos
conocidos como tokens. Un token consta de un tipo y un valor. Por
ejemplo, el texto '123' se representa como el token ('INTEGER', 123).

El siguiente conjunto de tokens son definidos.  El nombre sugerido del
token esta a la izquierda, un ejemplo del texto que coincida esta a la
derecha.

Palabras reservadas:
    VAR    : 'var'
    PRINT  : 'print'
    IF     : 'if'
    ELSE   : 'else'
    WHILE  : 'while'
    FUN    : 'fun'
    RETURN : 'return'
    TRUE   : 'true'
    FALSE  : 'false'

Identificadores/Nombres:
    IDENT  : Texto que inicia con una letra o '_', seguido por
             cualquier numero de letras, digitos o '_'.
             Ejemplo: 'abc', 'ABC', 'abc123', '_abc', 'a_b_c'

Literales (constantes):
    INTEGER : 123
    FLOAT   : 1.234
    STRING  : "esto es una cadena"

Operadores:
    PLUS    : '+'
    MINUS   : '-'
    TIMES   : '*'
    DIVIDE  : '/'
    LT      : '<'
    LE      : '<='
    GT      : '>'
    GE      : '>='
    EQ      : '=='
    NE      : '!='
    AND     : '&&'    (y logico, no a nivel de bits)
    OR      : '||'
    NOT     : '!'

Miselaneos:
    ASSIGN  : '='
    SEMI    : ';'
    LPAREN  : '('
    RPAREN  : ')'
    LBRACE  : '{'
    RBRACE  : '}'
    COMMA   : ','

Comentarios:
    //            Ignora el resto de la linea
    /* ... */     Ignora un bloque (no se permite anidamiento)

Errores: Su Analizador lexico opcionalmente puede reconocer y
reportar errores relacionados a caracteres ilegales, comentarios sin
terminar y otros problemas.
'''
from dataclasses import dataclass

# Definicion de Token
@dataclass
class Token:
    type   : str
    value  : str
    lineno : int = 0
    index  : int = 0


# Definiciones de tokens
literal_tokens = {
    '+' : 'PLUS',
    '-' : 'MINUS',
    '*' : 'TIMES',
    '/' : 'DIVIDE',
    '.' : 'POINT',
    ';' : 'SEMI',
    ',' : 'COMMA',
    '(' : 'LPAREN',
    ')' : 'RPAREN',
    '{' : 'LBRACE',
    '}' : 'RBRACE',
    '[' : 'LSqBra',
    ']' : 'RSqBra',
    '<' : 'LT',
    '>' : 'GT',
    '=' : 'ASSIGN',
    '==': 'EQ',
    '>=': 'GE',
    '<=': 'LE',
    '!=': 'NE',
    '&&': 'AND',
    '||': 'OR',
    '!' : 'NOT'
}

keywords = {
    'class', 'fun', 'var', 'for', 'if', 'else','print', 'return', 'while', 'true',
    'false', 'nil', 'this','super'
}

def addError(list,lineno):
    list.append("invalid syntax in line: "+str(lineno))

def tokenize(text: str) -> Token:
    lineno, n = 1, 0
    oneError=False
    errorList=[]

    while n < len(text) and not oneError:

        # newline
        if text[n] == '\n':
            n += 1
            lineno += 1
            continue

        # whitespace (' \t\n')
        if text[n].isspace():
            if text[n] == '\n':
                lineno += 1
            n += 1
            continue

        # Comentarios de bloque
        if text[n:n+2] == '/*':
            while n < len(text) and text[n:n+2] != '*/':
                if text[n] == '\n':
                    lineno += 1
                n += 1
            n += 2
            continue

        # Comentario de linea
        if text[n:n+2] == '//':
            while n < len(text) and text[n] != '\n':
                n += 1
            continue

        # Tokens de longitud 2
        if text[n:n+2] in literal_tokens:
            yield Token(literal_tokens[text[n:n+2]], text[n:n+2], lineno, n)
            n += 2
            continue

        # Tokens de longitud 1
        if text[n] in literal_tokens and not(text[n+1].isdigit()):
            yield Token(literal_tokens[text[n]], text[n], lineno, n)
            n += 1
            continue

        #keywords
        

        # Numeros enteros y de punto flotante
        if text[n].isdigit():
            start = n
            contLeftZeros=0

            while n < len(text) and text[n].isdigit() :
                n += 1
                if text[n]=='0' and contLeftZeros==0:
                    contLeftZeros=1
                if text[n]=='0' and contLeftZeros!=0:
                    addError(errorList,lineno)
                    oneError=True
            if n < len(text) and text[n] == '.':
                n += 1
                while n < len(text) and text[n].isdigit():
                    n += 1
                yield Token('FLOAT', text[start:n], lineno, start)
            else:
                yield Token('INTEGER', text[start:n], lineno, start)
            continue

        #Float .234 type
        if text[n]=='.' and text[n+1].isdigit():
            start = n
            n += 1
            while n < len(text) and text[n].isdigit():
                n += 1
            yield Token('FLOAT', text[start:n], lineno, start)
        continue

        n += 1
    print("\n\nErrors:")
    print(errorList)

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print('Usage: python tokenizer.py filename')
        exit(0)

    text = open(sys.argv[1]).read()

    for tok in tokenize(text):
        print(tok)
