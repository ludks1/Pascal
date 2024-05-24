class Error(Exception):
    class Error:
        def __init__(self, error_type, description, location):
            self.error_type = error_type
            self.description = description
            self.location = location
        def __str__(self):
            return f"{self.error_type}: {self.description} (línea {self.location[0]}, columna {self.location[1]})"


def report_error(error_type, description, location):
    error = Error(error_type, description, location)
    print(f"Error: {error_type}")
    print(f"Descripción: {description}")
    print(f"Ubicación: {location}")

# Errores léxicos


def not_valid_id(name, location):
    report_error("Error léxico", f"Identificador no válido: '{
                 name}'", location)


def not_valid_const(valor, location):
    report_error("Error léxico", f"Constante no válida: '{valor}'", location)


def not_valid_operator(simbol, location):
    report_error("Error léxico", f"Operador no válido: '{simbol}'", location)


# Errores sintácticos

def missing_parenthesis(location):
    report_error("Error sintáctico", "Falta un paréntesis", location)


def missing_semicolon(location):
    report_error("Error sintáctico", "Falta un punto y coma", location)


def invalid_instruction(simbol, location):
    report_error("Error sintáctico", f"Instrucción no válida: '{
                 simbol}'", location)


# Errores semánticos

def variable_not_defined(name, location):
    report_error("Error semántico",
                 f"Variable no declarada: '{name}'", location)


def incompatible_types(type1, type2, location):
    report_error("Error semántico", f"Tipos incompatibles: '{
                 type1}' y '{type2}'", location)


def assignment_to_expression(location):
    report_error("Error semántico",
                 "No se puede asignar un valor a una expresión", location)
