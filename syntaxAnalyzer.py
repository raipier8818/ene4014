class SyntaxAnalyzer():
    def __init__(self):    
        self.operators = ['+', '-', '*', '/']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.lexemes = []
        self.tokens = []
    
    def lexer(self, expression):
        i = 0
        while i < len(expression):
            if expression[i] in self.operators:
                self.lexemes.append(expression[i])
                self.tokens.append(expression[i])
                i += 1
            elif expression[i] in self.numbers:
                num = expression[i]
                i += 1
                while i < len(expression) and expression[i] in self.numbers:
                    num += expression[i]
                    i += 1
                self.lexemes.append(int(num))
                self.tokens.append("N")
            elif expression[i] == ' ':
                i += 1
            else:
                error = "Invalid character found: " + expression[i]
                raise Exception(error)
            
        self.lexemes.append('$')
        self.tokens.append('$')
        return self.lexemes, self.tokens

    def parser(self, params):
        # LR(1) Parser
        lexemes, tokens = params
        
        if lexemes is None or tokens is None:
            raise Exception("No lexemes or tokens found")
        
        if len(lexemes) != len(tokens):
            raise Exception("Lexemes and Tokens do not match")

        keys = []
        for i in range(len(lexemes)):
            keys.append((lexemes[i], tokens[i]))
        
        parsing_table = {
            (0, 'N') : (3, 'S'),
            (0, 'E') : (1, 'G'),
            (0, 'T') : (2, 'G'),
            (1, '+') : (4, 'S'),
            (1, '-') : (5, 'S'),
            (1, '$') : (0, 'A'),
            (2, '+') : (3, 'R'),
            (2, '-') : (3, 'R'),
            (2, '*') : (6, 'S'),
            (2, '/') : (7, 'S'),
            (2, '$') : (3, 'R'),
            (3, '+') : (6, 'R'),
            (3, '-') : (6, 'R'),
            (3, '*') : (6, 'R'),
            (3, '/') : (6, 'R'),
            (3, '$') : (6, 'R'),
            (4, 'N') : (3, 'S'),
            (4, 'T') : (8, 'G'),
            (5, 'N') : (3, 'S'),
            (5, 'T') : (9, 'G'),
            (6, 'N') : (10, 'S'),
            (7, 'N') : (11, 'S'),
            (8, '+') : (1, 'R'),
            (8, '-') : (1, 'R'),
            (8, '*') : (6, 'S'),
            (8, '/') : (7, 'S'),
            (8, '$') : (1, 'R'),
            (9, '+') : (2, 'R'),
            (9, '-') : (2, 'R'),
            (9, '*') : (6, 'S'),
            (9, '/') : (7, 'S'),
            (9, '$') : (2, 'R'),
            (10, '+') : (4, 'R'),
            (10, '-') : (4, 'R'),
            (10, '*') : (4, 'R'),
            (10, '/') : (4, 'R'),
            (10, '$') : (4, 'R'),
            (11, '+') : (5, 'R'),
            (11, '-') : (5, 'R'),
            (11, '*') : (5, 'R'),
            (11, '/') : (5, 'R'),
            (11, '$') : (5, 'R')
        }
        
        stack = [0]
        i = 0
        
        while i < len(keys):
            state = stack[-1]
            key = keys[i]
            
            print(state, key)
            
            if (state, key[0]) in parsing_table:    
                num, action = parsing_table[(state, key[0])]
                if action == 'S':
                    i += 1
                elif action == 'R':
                    if num == 1 or num == 2 or num == 4 or num == 5:
                        ET = stack[-6]
                        op = stack[-4]
                        TN = stack[-2]
                        
                        if ET[0] != 'E' or TN[0] != 'T':
                            raise Exception("Invalid syntax")
                        
                        if op == '+':
                            result = ('E', ET[1] + TN[1])
                        elif op == '-':
                            result = ('E', ET[1] - TN[1])
                        elif op == '*':
                            result = ('T', ET[1] * TN[1])
                        elif op == '/':
                            result = ('T', ET[1] / TN[1])
                        
                        stack = stack[:-6]
                        state, action = parsing_table[(stack[-1], result[0])]
                        if action == 'G':
                            stack.append(result)
                            stack.append(state)
                        else:
                            raise Exception("Invalid action")
                    if num == 3 or num == 6:
                        TN = stack[-2]
                        
                        stack = stack[:-2]
                        state, action = parsing_table[(stack[-1], TN[0])]
                        
                        if action == 'G':
                            stack.append(TN)
                            stack.append(state)
                        else:
                            raise Exception("Invalid action")
                        
                elif action == 'A':
                    return stack[-2][1]
                else:
                    raise Exception("Invalid action")
            else:
                raise Exception("Invalid syntax")                        
        return None


def main():
    
    while True:
        string = input(">> ")
        S = SyntaxAnalyzer()
        lexemes, tokens = S.lexer(string)
        print ("Lexemes:" + str(lexemes))
        print ("Tokens:" + str(tokens))
        
        value = S.parser((lexemes, tokens))
        print ("Value: " + str(value))
        
if __name__ == "__main__":
    main()