from Table import Table

class LRParser():
    def __init__(self, test=False) -> None:
        self.test = test
        
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
        
        table = Table("LR Parser", ["STACK", "INPUT", "ACTION"], [2])
        
        stack = [0]
        i = 0        
        stack_str = ""
        input_str = ""
        action_str = ""
        while i < len(keys):
            state = stack[-1]
            key = keys[i]
            
            stack_str = ""
            for s in stack:
                if isinstance(s, int):
                    stack_str += str(s) + " "
                else:
                    stack_str += str(s[1]) + " "
            stack_str = stack_str[:-1]
            
            input_str = ""
            for k in keys[i:]:
                input_str += str(k[1])
            
            if (state, key[1]) in parsing_table:    
                num, action = parsing_table[(state, key[1])]
                
                if action == 'S':
                    action_str = "Shift " + str(num)
                    stack.append(key)
                    stack.append(num)
                    i += 1
                elif action == 'R':
                    if num == 1 or num == 2 or num == 4 or num == 5:
                        ET = stack[-6]
                        op = stack[-4][0]
                        TN = stack[-2]
                        
                        if ET[1] != 'E' and ET[1] != 'T':
                            raise Exception("Invalid syntax")
                        
                        if TN[1] != 'N' and TN[1] != 'T':
                            raise Exception("Invalid syntax")

                        if op == '+':
                            result = (ET[0] + TN[0], 'E')
                        elif op == '-':
                            result = (ET[0] - TN[0], 'E')
                        elif op == '*':
                            result = (ET[0] * TN[0], 'T')
                        elif op == '/':
                            result = (ET[0] / TN[0], 'T')
                        else:   
                            raise Exception("Invalid operator " + str(op))
                            
                        stack = stack[:-6]
                        state, action = parsing_table[(stack[-1], result[1])]
                        
                        action_str = "Reduce " + str(num)
                        
                        if action == 'G':
                            action_str += " (Goto [" + str(state) + ", " + result[1] + "])"
                            stack.append(result)
                            stack.append(state)
                        else:
                            raise Exception("Invalid action")
                        
                    elif num == 3 or num == 6:
                        TN = stack[-2]                        
                        if TN[1] == 'N':
                            result = (TN[0], 'T')
                        elif TN[1] == 'T':
                            result = (TN[0], 'E')
                        else:
                            raise Exception("Invalid syntax")
                        
                        stack = stack[:-2]
                        state, action = parsing_table[(stack[-1], result[1])]
                        
                        action_str = "Reduce " + str(num)
                        
                        if action == 'G':
                            action_str += " (Goto [" + str(state) + ", " + result[1] + "])"
                            stack.append(result)
                            stack.append(state)
                        else:
                            raise Exception("Invalid action")
                        
                elif action == 'A':
                    action_str = "Accept"                    
                    table.insert([stack_str, input_str, action_str])
                    
                    if not self.test:
                        table.print_table()
                    return stack[-2][0]
                else:
                    raise Exception("Invalid action")
            else:
                raise Exception("Invalid syntax")     
            
            table.insert([stack_str, input_str, action_str])
            
        
        table.print_table()           
        return None