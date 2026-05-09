
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import tokenize
from parser import Parser
from semantic import SemanticAnalyzer
from ir import IRGenerator
from optimizer import Optimizer
from codegen import CodeGenerator

def compile_program(filename, debug=False):
    with open(filename, 'r') as f:
        code = f.read()

    tokens = tokenize(code)

    parser = Parser(tokens)
    ast = parser.parse()

    semantic = SemanticAnalyzer()
    semantic.analyze(ast)

    ir_gen = IRGenerator()
    ir_code = ir_gen.generate(ast)

    optimizer = Optimizer()
    optimized_ir = optimizer.optimize(ir_code)

    if debug:
        print("\nTOKENS")
        print(tokens)

        print("\nAST")
        print(ast)

        print("\nSYMBOL TABLE")
        print(semantic.symbol_table)

        print("\nIR")
        for ins in ir_code:
            print(ins)

        print("\nOPTIMIZED IR")
        for ins in optimized_ir:
            print(ins)

    generator = CodeGenerator(semantic.symbol_table)
    generator.execute(ast)

def interactive_mode():
    print("RetroLogo Interactive Mode")
    print("Type EXIT to quit")

    while True:
        line = input(">>> ")

        if line.upper() == "EXIT":
            break

        try:
            code = "START\n" + line + "\nEND"

            tokens = tokenize(code)
            parser = Parser(tokens)
            ast = parser.parse()

            semantic = SemanticAnalyzer()
            semantic.analyze(ast)

            generator = CodeGenerator(semantic.symbol_table)
            generator.execute(ast)

        except Exception as e:
            print("ERROR:", e)

if __name__ == "__main__":
    
    argparser = argparse.ArgumentParser()

    argparser.add_argument("file", nargs='?')
    argparser.add_argument("--debug", action="store_true")
    argparser.add_argument("--interactive", action="store_true")

    args = argparser.parse_args()

    if args.interactive:
        interactive_mode()

    elif args.file:
        compile_program(args.file, args.debug)

    else:
        print("Provide source file or use --interactive")
