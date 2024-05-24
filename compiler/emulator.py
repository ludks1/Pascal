import os
import sys
from scanner import Scanner
from parser_1 import Parser
from simulator import Simulator
from document import create_pdf, read_source_code


def usage():
    sys.stderr.write('Usage: Pascal filename\n')
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]

    source_code = read_source_code(filename)
    # Initialize scanner
    scanner = Scanner(1, 1, '', '', [], [], False, False, False, False)
    # Pass in file name, return list of tokens
    tokens = scanner.scan(filename)
    tokens.append(('EOF', 0, 0, 0))
    # Initialize parser
    output_dir = 'compiler/documentacion'
    output_pdf_path = os.path.join(output_dir, 'documentacion_codigo.pdf')
    create_pdf(source_code, output_pdf_path)
    print(f"Documentacion generada: {output_pdf_path}")
    try:
        parser = Parser(tokens, 0)
        result = parser.parse()
    except SyntaxError as e:
        print("Error de compilacion", e)
        sys.exit(1)
    # Return the AST using tokens
    ast = parser.parse()
    simulator = Simulator(ast['decorated_nodes'], ast['symtable'])
    try:
        simulator.simulate()
    except Exception as e:
        print("Error al momento de intentar la simulacion:", e)
        sys.exit(1)

    instructions = []
    for inst in ast['decorated_nodes']:
        instructions.append([inst['instruction'], inst['value']])
    print("\n")
    print("[Simulacion]: instrucciones:")
    print("\n")
    ip = 0
    for inst in instructions:
        if ip > 9:
            print("I" + str(ip) + ":     " + str(instructions[ip]))
        else:
            print("I" + str(ip) + ":      " + str(instructions[ip]))
        ip += 1
    print("\n")



    simulator.simulate()
