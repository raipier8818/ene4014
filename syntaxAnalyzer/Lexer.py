class Lexer:
    def __init__(self):
        self.operators = ['+', '-', '*', '/']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    # extract lexemes and tokens from the expression
    def lexer(self, expression):
        i = 0
        lexemes = []
        tokens = []
        
        while i < len(expression):
            # operations
            if expression[i] in self.operators:
                lexemes.append(expression[i])
                tokens.append(expression[i])
                i += 1
                
            # numbers
            elif expression[i] in self.numbers:
                num = expression[i]
                i += 1
                
                # find all numbers
                while i < len(expression) and expression[i] in self.numbers:
                    num += expression[i]
                    i += 1
                
                # convert to integer
                lexemes.append(int(num))
                tokens.append("N")
            
            # spaces
            elif expression[i] == ' ':
                i += 1
                
            # others (unknown)
            else:
                lexemes.append(expression[i])
                tokens.append("unknown")
                i += 1
            
        # add end of string
        lexemes.append('$')
        tokens.append('$')
        return lexemes, tokens