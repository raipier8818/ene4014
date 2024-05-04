class LLParser():
    def __init__(self, test=False) -> None:
        self.test = test
    
    def parser(self, params):
        # LL Parser
        lexemes, tokens = params
        
        if lexemes is None or tokens is None:
            raise Exception("No lexemes or tokens found")
        
        if len(lexemes) != len(tokens):
            raise Exception("Lexemes and Tokens do not match")
        
        keys = []
        for i in range(len(lexemes)):
            keys.append((lexemes[i], tokens[i]))
        
        i = 0
        
        print_buffer = ["Start!!"]
        
        # Right Recursive Grammar
        # E -> T E'
        # E' -> + T E' | - T E' | ε
        # T -> N T'
        # T' -> * N T' | / N T' | ε
        
        # EBNF Grammar
        # E -> T { + T | - T }
        # T -> N { * N | / N }
        # N -> number        
        
        def E():
            nonlocal i, keys, print_buffer
            print_buffer.append("enter E")
            
            if keys[i][1] != "N":
                raise Exception("Syntax Error")
            
            result = T()    
            
            while True:
                key = keys[i]
                if key[0] == '+':
                    i += 1
                    result += T()
                elif key[0] == '-':
                    i += 1
                    result -= T()
                else:
                    print_buffer.append("epsilon")
                    break
            print_buffer.append("exit E")
            return result
        
        def T():
            nonlocal i, keys, print_buffer
            print_buffer.append("enter T")
            
            if keys[i][1] != "N":
                raise Exception("Syntax Error")
            
            result = N()
            
            while True:
                key = keys[i]
                if key[0] == '*':
                    i += 1
                    result *= N()
                elif key[0] == '/':
                    i += 1
                    result /= N()
                else:
                    print_buffer.append("epsilon")
                    break
            print_buffer.append("exit T")
            return result
        
        def N():
            nonlocal i, keys
            key = keys[i]
            result = key[0]
            i += 1
            return result
        
        
        
        value = E()
        
        if not self.test:
            for line in print_buffer:
                print(line)
        
        return value