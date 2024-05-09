from Lexer import Lexer
from LLParser import LLParser
from LRParser import LRParser
from SyntaxAnalyzer import SyntaxAnalyzer
import random
import unittest

# Lexer test
class LexerTests(unittest.TestCase):    
    def setUp(self) -> None:
        self.__lexer = Lexer()
        return super().setUp()
    
    # Running test
    def test_run(self):
        print("\nLexer Run Test")
        expression = "1 + 2 * 3"
        expected_lexemes, expected_tokens = self.__lexer.lexer(expression)
        self.assertEqual(expected_lexemes, [1, '+', 2, '*', 3, '$'])
        self.assertEqual(expected_tokens, ['N', '+', 'N', '*', 'N', '$'])
            
    # Empty test
    def test_empty(self):
        print("\nLexer Empty Test")
        expression = ""
        expected_lexemes, expected_tokens = self.__lexer.lexer(expression)
        self.assertEqual(expected_lexemes, ['$'])
        self.assertEqual(expected_tokens, ['$'])
    
    # Single test
    def test_single(self):
        print("\nLexer Single Test")
        expression = "1"
        expected_lexemes, expected_tokens = self.__lexer.lexer(expression)
        self.assertEqual(expected_lexemes, [1, '$'])
        self.assertEqual(expected_tokens, ['N', '$'])
        
    # Random test
    def test_random(self):
        print("\nLexer Random Test")
        expression = ""
        tokens = []
        
        for i in range(1000):
            number = str(random.randint(0, 9))
            op = random.choice(['+', '-', '*', '/'])
            expression += number + op
            tokens.append('N')
            tokens.append(op)
            
        expression = expression[:-1]
        tokens = tokens[:-1]
        tokens.append('$')
        
        expected_lexemes, expected_tokens = self.__lexer.lexer(expression)
        self.assertEqual(len(expected_lexemes), len(expected_tokens))
        self.assertEqual("".join([str(i) for i in expected_lexemes[:-1]]), expression)
        self.assertEqual(expected_tokens, tokens)
    
    # Invalid test
    def test_invalid(self):
        print("\nLexer Invalid Test")
        expression = "1 + 2 * 3 &"
        expected_lexemes, expected_tokens = self.__lexer.lexer(expression)
        self.assertEqual(expected_lexemes, [1, '+', 2, '*', 3, '&', '$'])
        self.assertEqual(expected_tokens, ['N', '+', 'N', '*', 'N', 'unknown', '$'])

# LLParser test
class LLParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__lexer = Lexer()
        self.__llparser = LLParser(test=True)
        return super().setUp()
    
    # Running test
    def test_run(self):
        print("\nLLParser Run Test")
        expression = "1 + 2 * 3"
        lexemes, tokens = self.__lexer.lexer(expression)        
        expected_value = self.__llparser.parser((lexemes, tokens))
        self.assertEqual(expected_value, eval(expression))
    
    # Empty test
    def test_empty(self):
        print("\nLLParser Empty Test")
        expression = ""
        lexemes, tokens = self.__lexer.lexer(expression)
        with self.assertRaises(Exception):
            expected_value = self.__llparser.parser((lexemes, tokens))
        
    # Single test
    def test_single(self):
        print("\nLLParser Single Test")
        expression = "1"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '$'])
        self.assertEqual(tokens, ['N', '$'])
        
        expected_value = self.__llparser.parser((lexemes, tokens))
        self.assertEqual(expected_value, eval(expression))
    
    # Zero division test
    def test_zero_division(self):
        print("\nLLParser Zero Division Test")
        expression = "1 / 0"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '/', 0, '$'])
        self.assertEqual(tokens, ['N', '/', 'N', '$'])
        
        with self.assertRaises(ZeroDivisionError):
            expected_value = self.__llparser.parser((lexemes, tokens))    
    
    # Random test
    def test_random(self):
        print("\nLLParser Random Test")
        expression = ""
        for i in range(1000):
            expression += str(random.randint(1, 9))
            expression += random.choice(['+', '-', '*', '/'])
        expression = expression[:-1]
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(len(lexemes), len(tokens))
        
        expected_value = self.__llparser.parser((lexemes, tokens))
        # check expected_value int or float
        self.assertTrue(isinstance(expected_value, int) or isinstance(expected_value, float))
        self.assertEqual(expected_value, eval(expression))
    
    # Invalid test
    def test_invalid(self):
        print("\nLLParser Invalid Test")
        expression = "1 + 2 * 3 &"
        with self.assertRaises(Exception):
            lexemes, tokens = self.__lexer.lexer(expression)   
            expected_value = self.__llparser.parser((lexemes, tokens))
            

# LRParser test
class LRParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__lexer = Lexer()
        self.__lrparser = LLParser(test=True)
        return super().setUp()
    
    # Running test
    def test_run(self):
        print("\nLRParser Run Test")
        expression = "1 + 2 * 3"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '+', 2, '*', 3, '$'])
        self.assertEqual(tokens, ['N', '+', 'N', '*', 'N', '$'])
        
        expected_value = self.__lrparser.parser((lexemes, tokens))
        self.assertEqual(expected_value, 7)
    
    # Empty test
    def test_empty(self):
        print("\nLRParser Empty Test")
        expression = ""
        lexemes, tokens = self.__lexer.lexer(expression)
        with self.assertRaises(Exception):
            expected_value = self.__lrparser.parser((lexemes, tokens))
    
    # Single test
    def test_single(self):
        print("\nLRParser Single Test")
        expression = "1"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '$'])
        self.assertEqual(tokens, ['N', '$'])
        
        expected_value = self.__lrparser.parser((lexemes, tokens))
        self.assertEqual(expected_value, 1)
        
    # Zero division test
    def test_zero_division(self):
        print("\nLRParser Zero Division Test")
        expression = "1 / 0"
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(lexemes, [1, '/', 0, '$'])
        self.assertEqual(tokens, ['N', '/', 'N', '$'])
        
        with self.assertRaises(ZeroDivisionError):
            expected_value = self.__lrparser.parser((lexemes, tokens))
    
    # Random test      
    def test_random(self):
        print("\nLRParser Random Test")
        expression = ""
        for i in range(1000):
            expression += str(random.randint(1, 9))
            expression += random.choice(['+', '-', '*', '/'])
        expression = expression[:-1]
        lexemes, tokens = self.__lexer.lexer(expression)
        self.assertEqual(len(lexemes), len(tokens))
        
        expected_value = self.__lrparser.parser((lexemes, tokens))
        # check expected_value int or float
        self.assertTrue(isinstance(expected_value, int) or isinstance(expected_value, float))
        self.assertEqual(expected_value, eval(expression))
    
    # Invalid test    
    def test_invalid(self):
        print("\nLRParser Invalid Test")
        expression = "1 + 2 * 3 &"
        with self.assertRaises(Exception):
            lexemes, tokens = self.__lexer.lexer(expression)   
            expected_value = self.__lrparser.parser((lexemes, tokens))

class ParserTests(unittest.TestCase):
    def setUp(self):
        self.__lexer = Lexer()
        self.__llparser = LLParser(test=True)
        self.__lrparser = LRParser(test=True)
        return super().setUp()
    
    def test_result(self):
        print("\nSyntaxAnalyzer Result Test")
        
        expression = ""
        for i in range(1000):
            expression += str(random.randint(1, 9))
            expression += random.choice(['+', '-', '*', '/'])
        expression = expression[:-1]
        lexemes, tokens = self.__lexer.lexer(expression)
        
        # LL Parser Result
        ll_expected_value = self.__llparser.parser((lexemes, tokens))
        
        # LR Parser Result
        lr_expected_value = self.__lrparser.parser((lexemes, tokens))
        self.assertEqual(ll_expected_value, lr_expected_value)

if __name__ == "__main__":
    unittest.main()