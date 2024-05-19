import sys
from prettytable import PrettyTable
from error import Error, report_error


class Simulator(object):

    def __init__(self, ast, symtable):
        self.ast = ast
        self.stack = []
        self.symtable = symtable
        self.ip = 0

    def simulate(self):
        while True:
            try:
                if self.ast[self.ip]['instruction'] == 'op_push':
                    if self.ast[self.ip]['token'] == 'TK_IDENTIFIER':
                        self.pushi(self.ast[self.ip]['value'])
                    else:
                        self.push(self.ast[self.ip]['value'])
                elif self.ast[self.ip]['instruction'] == 'op_or':
                    self.op_or()
                elif self.ast[self.ip]['instruction'] == 'op_and':
                    self.op_and()
                elif self.ast[self.ip]['instruction'] == 'op_xor':
                    self.op_xor()
                elif self.ast[self.ip]['instruction'] == 'op_not':
                    self.op_not()
                elif self.ast[self.ip]['instruction'] == 'op_mod':
                    self.mod()
                elif self.ast[self.ip]['instruction'] == 'op_less':
                    self.op_less()
                elif self.ast[self.ip]['instruction'] == 'op_greater':
                    self.op_greater()
                elif self.ast[self.ip]['instruction'] == 'op_less_equals':
                    self.op_lesseq()
                elif self.ast[self.ip]['instruction'] == 'op_greater_equals':
                    self.op_greatereq()
                elif self.ast[self.ip]['instruction'] == 'op_not_equals':
                    self.op_noteq()
                elif self.ast[self.ip]['instruction'] == 'op_equals':
                    self.op_equals()
                elif self.ast[self.ip]['instruction'] == 'op_div_float':
                    self.div_float()
                elif self.ast[self.ip]['instruction'] == 'op_add':
                    self.add()
                elif self.ast[self.ip]['instruction'] == 'op_pop':
                    self.pop(self.ast[self.ip]['value'])
                elif self.ast[self.ip]['instruction'] == 'op_minus':
                    self.minus()
                elif self.ast[self.ip]['instruction'] == 'op_mult':
                    self.mult()
                elif self.ast[self.ip]['instruction'] == 'op_halt':
                    self.halt()
                elif self.ast[self.ip]['instruction'] == 'op_jfalse':
                    self.op_jfalse(self.ast[self.ip]['value'])
                elif self.ast[self.ip]['instruction'] == 'op_jmp':
                    self.op_jmp(self.ast[self.ip]['value'])
                elif self.ast[self.ip]['instruction'] == 'op_jtrue':
                    self.op_jtrue(self.ast[self.ip]['value'])
                elif self.ast[self.ip]['instruction'] == 'op_writeln':
                    self.writeln()
                else:
                    line, column = self.ast[self.ip]['line'], self.ast[self.ip]['column']
                    report_error("Error semántico",
                                 "Instrucción desconocida", (line, column))
                    break
                self.ip += 1
                # print self.stack
                # print "\n"
            except IndexError:
                if self.ip >= len(self.ast):
                    report_error("Error de ejecución",
                                 "Fin del programa", (self.ip, None))
                    break
                else:
                    report_error("Error de ejecución",
                                 "Índice fuera de rango", (self.ip, None))
                    break
            except TypeError as e:
                # Handle type errors (e.g., incompatible operand types)
                line, column = self.ast[self.ip]['line'], self.ast[self.ip]['column']
                report_error("Error semántico", f"Error de tipo: {
                             str(e)}", (line, column))
                break
            except Exception as e:
                # Handle other unexpected errors
                print(f"Error durante la simulación: {e}")
                sys.exit(1)

    def printer(self, iterator, field_names, storage, data):
        table = PrettyTable()
        table.field_names = field_names
        for datum in data:
            storage.append(iterator)
            for k, v in datum.items():
                if str(k) == 'NAME':
                    storage.append(v)
                if str(k) == 'VALUE':
                    storage.append(v)
                if str(k) == 'TYPE':
                    storage.append(v)
                if str(k) == 'ADDRESS':
                    storage.append(hex(v))
            table.add_row(storage)
            del storage[:]
            iterator += 1
        return table

    def writeln(self):
        val = self.stack.pop()
        print(val)

    def op_jfalse(self, instruction):
        bool_val = self.stack.pop()
        if bool_val == False:
            self.ip = instruction - 1

    def op_jmp(self, instruction):
        self.ip = instruction - 1

    def op_jtrue(self, instruction):
        bool_val = self.stack.pop()
        if bool_val == True:
            self.ip = instruction - 1

    def halt(self):
        print("\nTABLA FINAL: ")
        print("\n")
        print(self.printer(1, ['NUMERO', 'IDENTIFICADOR',
              'QUE ES?', 'VALOR', 'RUTA MEMORIA'], [], self.symtable))
        sys.exit(0)

    def op_lesseq(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) <= int(op_2)
        self.push(val)
        return

    def op_noteq(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) != int(op_2)
        self.push(val)
        return

    def op_equals(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) == int(op_2)
        self.push(val)
        return

    def op_greatereq(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) >= int(op_2)
        self.push(val)
        return

    def op_greater(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) > int(op_2)
        self.push(val)
        return

    def op_less(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) < int(op_2)
        self.push(val)
        return

    def op_not(self):
        op_1 = self.stack.pop()
        val = not int(op_1)
        self.push(val)
        return

    def op_and(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) and int(op_2)
        self.push(val)
        return

    def op_xor(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) ^ int(op_2)
        self.push(val)
        return

    def op_or(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) or int(op_2)
        self.push(val)
        return

    def mod(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) % int(op_2)
        self.push(val)
        return

    def div_float(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) / int(op_2)
        self.push(val)
        return

    def pushi(self, value):
        for var in self.symtable:
            if var['NAME'] == value:
                self.stack.insert(0, var['VALUE'])
        return

    def push(self, value):
        self.stack.insert(0, value)
        return

    def pop(self, value):
        op_1 = self.stack.pop()
        for var in self.symtable:
            if var['NAME'] == value:
                var['VALUE'] = op_1
        return

    def mult(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_2) * int(op_1)
        self.push(val)
        return

    def add(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_2) + int(op_1)
        self.push(val)
        return

    def minus(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_2) - int(op_1)
        self.push(val)
        return

    def type(self, value):
        return type(value)
