class LLParser():
    def __init__(self, test=False) -> None:
        # test : If False, then print the parsing process
        self.test = test
    
    # LL Parser
    def parser(self, params):
        lexemes, tokens = params
        
        # Check if lexemes and tokens are not empty
        if lexemes is None or tokens is None:
            raise Exception("No lexemes or tokens found")
        
        # Check if lexemes and tokens are not same length
        if len(lexemes) != len(tokens):
            raise Exception("Lexemes and Tokens do not match")
        
        # Set lexemes and tokens to keys used in parsing process
        # keys : (lexeme, token) 
        keys = []
        for i in range(len(lexemes)):
            # Check if token is unknown
            if tokens[i] == "unknown":
                raise Exception("Unknown token found")
            keys.append((lexemes[i], tokens[i]))
        
        # index of keys
        i = 0
        print_buffer = ["Start!!"]
        
        # Right Recursive Grammar
        # E -> T E'
        # E' -> + T E' | - T E' | ε
        # T -> N T'
        # T' -> * N T' | / N T' | ε
        
        # EBNF Grammar (I'll use this)
        # E -> T { + T | - T }
        # T -> N { * N | / N }
        # N -> number        
        
        def E():
            nonlocal i, keys, print_buffer
            print_buffer.append("enter E")
            
            # Get value of N
            result = T()    
            
            # Check if lexeme is operator
            while True:
                key = keys[i]
                if key[0] == '+':
                    # find next lexeme
                    i += 1
                    result += T()
                elif key[0] == '-':
                    # find next lexeme
                    i += 1
                    result -= T()
                    
                # If no operator, then break
                else:
                    print_buffer.append("epsilon")
                    break
            print_buffer.append("exit E")
            return result
        
        def T():
            nonlocal i, keys, print_buffer
            print_buffer.append("enter T")
            
            # Get value of N
            result = N()
            
            # Check if lexeme is operator
            while True:
                key = keys[i]
                if key[0] == '*':
                    # find next lexeme
                    i += 1
                    result *= N()
                elif key[0] == '/':
                    # find next lexeme
                    i += 1
                    result /= N()
                    
                # If no operator, then break
                else:
                    print_buffer.append("epsilon")
                    break
            print_buffer.append("exit T")
            return result
        
        def N():
            nonlocal i, keys
            
            # Check if lexeme is number
            if keys[i][1] != "N":
                raise Exception("Syntax Error")
            
            key = keys[i]
            result = key[0]
            
            # find next lexeme
            i += 1
            return result
        
        
        
        value = E()
        
        if not self.test:
            for line in print_buffer:
                print(line)
        
        return value