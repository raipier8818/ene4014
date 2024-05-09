import sys
import Lexer
import LLParser
import LRParser

class SyntaxAnalyzer:
    def __init__(self, lexer, parser) -> None:
        self.__lexer = lexer
        self.__parser = parser
        
    def lexer(self, expression):
        return self.__lexer.lexer(expression)
    
    def parser(self, params):
        try:
            return self.__parser.parser(params)
        except Exception as e:
            return "unknown"
        
def main():
    L = Lexer.Lexer()
    LLP = LLParser.LLParser()
    LRP = LRParser.LRParser()
    
    # SyntaxAnalyzer using LL Parser
    # SA = SyntaxAnalyzer(L, LLP)
    
    # SyntaxAnalyzer using LR Parser
    SA = SyntaxAnalyzer(L, LRP)
    
    while True:
        try:
            string = input(">> ")
            if string == "":
                continue
            
            lexemes, tokens = SA.lexer(string)
            print ("Lexemes:" + str(lexemes))
            print ("Tokens:" + str(tokens))
            
            value = SA.parser((lexemes, tokens))
            print ("Result: " + str(value))
        except Exception as e:
            print(e)
        
        
if __name__ == "__main__":
    main()