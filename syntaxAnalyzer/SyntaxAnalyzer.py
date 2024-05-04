import Lexer
import LLParser
import LRParser

class SyntaxAnalyzer:
    def __init__(self, lexer, parser) -> None:
        self.__lexer = lexer
        self.__parser = parser
        
    def lexer(self, expression):
        try:
            return self.__lexer.lexer(expression)
        except Exception as e:
            return None, None
    
    def parser(self, params):
        try:
            return self.__parser.parser(params)
        except Exception as e:
            return None    
        
def main():
    L = Lexer.Lexer()
    LLP = LLParser.LLParser()
    LRP = LRParser.LRParser()
    LLS = SyntaxAnalyzer(L, LLP)
    while True:
        try:
            string = input(">> ")
            if string == "":
                continue
            
            lexemes, tokens = LLS.lexer(string)
            print ("Lexemes:" + str(lexemes))
            print ("Tokens:" + str(tokens))
            
            value = LLS.parser((lexemes, tokens))
            print ("Result: " + str(value))
        except Exception as e:
            print(e)
        
        
if __name__ == "__main__":
    main()