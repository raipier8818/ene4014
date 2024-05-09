from Table import Table

class LRParser():
    def __init__(self, test=False) -> None:
        self.test = test
        
    def parser(self, params):
        # LR(1) Parser
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
            keys.append((lexemes[i], tokens[i]))
        
        # Parsing Table
        # (state, symbol) : (next_state, action)
        # action : S (Shift), R (Reduce), G (Goto), A (Accept)
        # (n, 'S') : Shift next state n
        # (n, 'R') : Reduce using rule n
        # (n, 'G') : Goto next state n
        # (0, 'A') : Accept (actually 0 is not used)
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
        
        # Create table for processing output
        table = Table("LR Parser", ["STACK", "INPUT", "ACTION"], [2])
        
        # set initial values used in table
        stack_str = ""
        input_str = ""
        action_str = ""
        
        # initial stack
        stack = [0]
        
        # initial index
        i = 0        
        
        while i < len(keys):
            # Get current state (top of stack)
            state = stack[-1]
            
            # Get current key (first lexeme of input)
            key = keys[i]
            
            # Set stack and input strings for table
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
            
            # Check if current state and key is in parsing table
            if (state, key[1]) in parsing_table:    
                num, action = parsing_table[(state, key[1])]
                
                # Check if action is Shift
                if action == 'S':
                    # In this case, num is next state
                    # Set action string for table
                    action_str = "Shift " + str(num)
                    
                    # Push key to stack
                    stack.append(key)
                    
                    # Push next state to stack
                    stack.append(num)
                    
                    # Move to next key
                    i += 1
                    
                elif action == 'R':
                    # In this case, num is rule number
                    # Set action string for table
                    action_str = "Reduce " + str(num)
                    
                    # Check if rule number is in form like "A -> B op C"
                    if num == 1 or num == 2 or num == 4 or num == 5:
                        # stack = [..., ET, state, op, state, TN, state]
                        # Get top 3 key elements from stack (lexemes)
                        # Ignore 3 elements from stack (states)
                        
                        # ET : key of E or T
                        ET = stack[-6]
                        
                        # op : key of operator
                        op = stack[-4][0]
                        
                        # TN : key of T or N
                        TN = stack[-2]
                        
                        # Check ET valid
                        if ET[1] != 'E' and ET[1] != 'T':
                            raise Exception("Invalid syntax")
                        
                        # Check TN valid
                        if TN[1] != 'N' and TN[1] != 'T':
                            raise Exception("Invalid syntax")

                        # Calculate result based on operator
                        if op == '+':
                            result = (ET[0] + TN[0], 'E')
                        elif op == '-':
                            result = (ET[0] - TN[0], 'E')
                        elif op == '*':
                            result = (ET[0] * TN[0], 'T')
                        elif op == '/':
                            result = (ET[0] / TN[0], 'T')
                            
                        # Check operator not valid
                        else:   
                            raise Exception("Invalid operator " + str(op))
                        
                        # pop 6 elements from stack
                        stack = stack[:-6]
                        
                        # Get next state from stack (Goto)
                        state, action = parsing_table[(stack[-1], result[1])]
                        
                        if action == 'G':
                            # Set action string for table (add Goto)
                            action_str += " (Goto [" + str(state) + ", " + result[1] + "])"
                            
                            # Push result to stack
                            stack.append(result)
                            
                            # Push next state to stack
                            stack.append(state)
                        else:
                            raise Exception("Invalid action")
                        
                    # Check if grammer number is in form like "A -> B"
                    elif num == 3 or num == 6:
                        # stack = [..., TN, state]
                        # Get top key element from stack (lexemes)
                        TN = stack[-2]                        
                        
                        # Check TN valid and set token to use grammer
                        if TN[1] == 'N':
                            result = (TN[0], 'T')
                        elif TN[1] == 'T':
                            result = (TN[0], 'E')
                        else:
                            raise Exception("Invalid syntax")
                        
                        # pop 2 elements from stack
                        stack = stack[:-2]
                        
                        # Get next state from stack (Goto)
                        state, action = parsing_table[(stack[-1], result[1])]
                        
                        # Check if action is Goto
                        if action == 'G':
                            # Set action string for table (add Goto)
                            action_str += " (Goto [" + str(state) + ", " + result[1] + "])"
                            
                            # Push result to stack
                            stack.append(result)
                            
                            # Push next state to stack
                            stack.append(state)
                        else:
                            raise Exception("Invalid action")
                
                # Check if action is Accept
                # In this case, num is 0 (not used)
                elif action == 'A':
                    # Set action string for table
                    action_str = "Accept"        
                    # Insert all strings to table            
                    table.insert([stack_str, input_str, action_str])
                    
                    # Print table if not test
                    if not self.test:
                        table.print_table()
                        
                    # Return result
                    return stack[-2][0]
                else:
                    raise Exception("Invalid action")
            else:
                raise Exception("Invalid syntax")     
            
            # Insert all strings to table
            table.insert([stack_str, input_str, action_str])
            
        # Print table if not test (not Accepted)
        table.print_table()           
        return None