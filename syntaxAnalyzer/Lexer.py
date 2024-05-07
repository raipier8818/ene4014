class Lexer:
    def __init__(self):
        self.operators = ['+', '-', '*', '/']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def lexer(self, expression):
            i = 0
            lexemes = []
            tokens = []
            while i < len(expression):
                if expression[i] in self.operators:
                    lexemes.append(expression[i])
                    tokens.append(expression[i])
                    i += 1
                elif expression[i] in self.numbers:
                    num = expression[i]
                    i += 1
                    while i < len(expression) and expression[i] in self.numbers:
                        num += expression[i]
                        i += 1
                    lexemes.append(int(num))
                    tokens.append("N")
                elif expression[i] == ' ':
                    i += 1
                else:
                    lexemes.append(expression[i])
                    tokens.append("unknown")
                    i += 1
                
            lexemes.append('$')
            tokens.append('$')
            return lexemes, tokens