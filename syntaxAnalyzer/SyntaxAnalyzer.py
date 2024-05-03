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
        return self.__parser.parser(params)        
        
def main():
    L = Lexer.Lexer()
    LLP = LLParser.LLParser()
    LRP = LRParser.LRParser()
    LLS = SyntaxAnalyzer(L, LRP)
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