from Lexer import Lexer
from LLParser import LLParser
import random
import unittest


class LexerTests(unittest.TestCase):    
    def setUp(self) -> None:
        self.__lexer = Lexer()
        return super().setUp()
    
    def test_run(self):
        print("\nLexer Run Test")
        expression = "1 + 2 * 3"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '+', 2, '*', 3, '$'])
        self.assertEqual(tokens, ['N', '+', 'N', '*', 'N', '$'])
    
    def test_empty(self):
        print("\nLexer Empty Test")
        expression = ""
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, ['$'])
        self.assertEqual(tokens, ['$'])
    
    def test_single(self):
        print("\nLexer Single Test")
        expression = "1"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '$'])
        self.assertEqual(tokens, ['N', '$'])
        
    def test_random(self):
        print("\nLexer Random Test")
        expression = ""
        for i in range(1000):
            expression += str(random.randint(0, 9))
            expression += random.choice(['+', '-', '*', '/'])
        expression = expression[:-1]
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(len(lexemes), len(tokens))
    
    def test_invalid(self):
        print("\nLexer Invalid Test")
        expression = "1 + 2 * 3 &"
        with self.assertRaises(Exception):
            lexemes, tokens = self.__lexer.lexer(expression)   

class LLParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__lexer = Lexer()
        self.__llparser = LLParser(test=True)
        return super().setUp()
    
    def test_run(self):
        print("\nLLParser Run Test")
        expression = "1 + 2 * 3"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '+', 2, '*', 3, '$'])
        self.assertEqual(tokens, ['N', '+', 'N', '*', 'N', '$'])
        
        value = self.__llparser.parser((lexemes, tokens))
        self.assertEqual(value, 7)
    
    def test_empty(self):
        print("\nLLParser Empty Test")
        expression = ""
        lexemes, tokens = self.__lexer.lexer(expression)
        with self.assertRaises(Exception):
            value = self.__llparser.parser((lexemes, tokens))
        
        
    def test_single(self):
        print("\nLLParser Single Test")
        expression = "1"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '$'])
        self.assertEqual(tokens, ['N', '$'])
        
        value = self.__llparser.parser((lexemes, tokens))
        self.assertEqual(value, 1)
    
    def test_zero_division(self):
        print("\nLLParser Zero Division Test")
        expression = "1 / 0"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '/', 0, '$'])
        self.assertEqual(tokens, ['N', '/', 'N', '$'])
        
        with self.assertRaises(ZeroDivisionError):
            value = self.__llparser.parser((lexemes, tokens))    
    
    def test_random(self):
        print("\nLLParser Random Test")
        expression = ""
        for i in range(1000):
            expression += str(random.randint(1, 9))
            expression += random.choice(['+', '-', '*', '/'])
        expression = expression[:-1]
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(len(lexemes), len(tokens))
        
        value = self.__llparser.parser((lexemes, tokens))
        # check value int or float
        self.assertTrue(isinstance(value, int) or isinstance(value, float))
    
    def test_invalid(self):
        print("\nLLParser Invalid Test")
        expression = "1 + 2 * 3 &"
        with self.assertRaises(Exception):
            lexemes, tokens = self.__lexer.lexer(expression)   
            value = self.__llparser.parser((lexemes, tokens))
            
            
class LRParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__lexer = Lexer()
        self.__lrparser = LLParser(test=True)
        return super().setUp()
    
    def test_run(self):
        print("\nLRParser Run Test")
        expression = "1 + 2 * 3"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '+', 2, '*', 3, '$'])
        self.assertEqual(tokens, ['N', '+', 'N', '*', 'N', '$'])
        
        value = self.__lrparser.parser((lexemes, tokens))
        self.assertEqual(value, 7)
        
    def test_empty(self):
        print("\nLRParser Empty Test")
        expression = ""
        lexemes, tokens = self.__lexer.lexer(expression)
        with self.assertRaises(Exception):
            value = self.__lrparser.parser((lexemes, tokens))
            
    def test_single(self):
        print("\nLRParser Single Test")
        expression = "1"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '$'])
        self.assertEqual(tokens, ['N', '$'])
        
        value = self.__lrparser.parser((lexemes, tokens))
        self.assertEqual(value, 1)
        
    def test_zero_division(self):
        print("\nLRParser Zero Division Test")
        expression = "1 / 0"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '/', 0, '$'])
        self.assertEqual(tokens, ['N', '/', 'N', '$'])
        
        with self.assertRaises(ZeroDivisionError):
            value = self.__lrparser.parser((lexemes, tokens))
            
    def test_random(self):
        print("\nLRParser Random Test")
        expression = ""
        for i in range(1000):
            expression += str(random.randint(1, 9))
            expression += random.choice(['+', '-', '*', '/'])
        expression = expression[:-1]
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(len(lexemes), len(tokens))
        
        value = self.__lrparser.parser((lexemes, tokens))
        # check value int or float
        self.assertTrue(isinstance(value, int) or isinstance(value, float))
        
    def test_invalid(self):
        print("\nLRParser Invalid Test")
        expression = "1 + 2 * 3 &"
        with self.assertRaises(Exception):
            lexemes, tokens = self.__lexer.lexer(expression)   
            value = self.__lrparser.parser((lexemes, tokens))

                
    
if __name__ == "__main__":
    unittest.main()