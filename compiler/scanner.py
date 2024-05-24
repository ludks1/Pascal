from prettytable import PrettyTable


class Scanner(object):
    def __init__(self, curr_row, curr_col, curr_token, curr_val, tokens, metadata, comment, string, numeric, real):
        self.curr_row = curr_row
        self.curr_col = curr_col
        self.curr_token = curr_token
        self.curr_val = curr_val
        self.tokens = tokens
        self.metadata = metadata
        self.comment = comment
        self.string = string
        self.numeric = numeric
        self.real = real

    # ----------------------------------------
    #               SCANNER
    # ----------------------------------------

    def scan(self, source):
        # Reads <source program> and builds tokens.
        text = open(source, 'r').readlines()
        for line in text:
            for char in line:
                # Handle comments
                if self.comment:
                    self.handle_comments(char)
                    if self.to_ascii(char) == 13:
                        self.curr_col = 1
                        self.curr_row += 1
                    self.curr_col += 1

                # Handle strings
                elif self.string:
                    self.string_builder(char)
                    if self.to_ascii(char) == 13:
                        self.curr_col = 1
                        self.curr_row += 1
                    self.curr_col += 1

                # Handle digits
                elif self.numeric:
                    self.numeric_builder(char)
                    if self.to_ascii(char) == 13:
                        self.curr_col = 1
                        self.curr_row += 1
                    self.curr_col += 1

                # Handle other cases
                else:
                    self.build_string(char)
                    # Handle carriage returns
                    if self.to_ascii(char) == 13:
                        self.curr_col = 1
                        self.curr_row += 1
                    self.curr_col += 1

        # Print out metadata
        print("\n")
        print("[Scanner]: Lista de tokens")
        print(self.printer(1, ['NUMERO', 'TOKEN',
              'TIPO', 'VALOR', 'FILA'], [], self.metadata))
        # print(self.tokens)
        return self.tokens

    # ----------------------------------------
    #             NUMERIC STATE
    # ----------------------------------------

    def numeric_builder(self, char):
        # If char is a number, keep building number string
        if self.to_ascii(char) >= 48 and self.to_ascii(char) <= 57:
            self.curr_val += char

        # Character is a symbol/space, time to build token
        if (self.to_ascii(char) > 57 or self.to_ascii(char) <= 32):
            self.numeric = False
            if self.real:
                self.tokens.append(
                    ('TK_REAL', self.curr_val, self.curr_row, self.curr_col - 1))
                self.metadata.append(
                    {'TOKEN': 'TK_REAL', 'VALUE': self.curr_val, 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                self.curr_val = ''
                self.real = False
                return
            else:
                self.tokens.append(
                    ('TK_INTEGER', self.curr_val, self.curr_row, self.curr_col - 1))
                self.metadata.append(
                    {'TOKEN': 'TK_INTEGER', 'VALUE': self.curr_val, 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                self.curr_val = ''
                return

        # If Character is a dot, it can be a real
        if self.to_ascii(char) == 46:
            self.curr_val += char
            self.real = True

    # ----------------------------------------
    #              STRING STATE
    # ----------------------------------------

    def string_builder(self, char):
        # If char is a quote ...
        if self.to_ascii(char) == 39:
            self.curr_val += char
            self.string = False
            self.tokens.append(('TK_STRING', self.curr_val,
                               self.curr_row, self.curr_col))
            self.metadata.append(
                {'TOKEN': 'TK_STRING', 'VALUE': self.curr_val, 'ROW': self.curr_row, 'COL': self.curr_col})
            self.curr_val = ''
            return

        # Char is not a quote, so keep building string
        else:
            self.curr_val += char
            return

    def handle_comments(self, char):
        # If char is * ...
        if self.to_ascii(char) == 42:
            self.curr_token = 'TK_MULT'
            return

        # If char is ) ...
        if self.to_ascii(char) == 41:
            # If there is no current token
            if not self.curr_token:
                pass

            # If there is a current token, it has to be *
            if self.curr_token == 'TK_MULT':
                self.comment = False
                self.tokens.append(('TK_END_COMMENT', '*)',
                                   self.curr_row, self.curr_col))
                self.metadata.append(
                    {'TOKEN': 'TK_END_COMMENT', 'VALUE': '*)', 'ROW': self.curr_row, 'COL': self.curr_col})
                self.curr_token = ''

        # We have not yet ended our comment section
        pass

    # ----------------------------------------
    #             PRETTY PRINTER
    # ----------------------------------------

    def printer(self, iterator, field_names, storage, data):
        table = PrettyTable()
        table.field_names = field_names
        for datum in data:
            storage.append(iterator)
            for k, v in datum.items():
                if str(k) == 'TOKEN':
                    storage.append(v)
                if str(k) == 'ROW':
                    storage.append(v)
                if str(k) == 'VALUE':
                    storage.append(v)
                if str(k) == 'COL':
                    storage.append(v)
            table.add_row(storage)
            del storage[:]
            iterator += 1
        return table

    # ----------------------------------------
    #            HELPER METHODS
    # ----------------------------------------

    def handle_numeric(self, char):
        return char.isdigit()

    def lookup(self, table, key):
        return table[key]

    def to_ascii(self, char):
        return ord(char)

    def to_lower(self, char):
        return char.lower()

    def to_upper(self, char):
        return char.upper()

    def alphanumeric(self, char):
        return char.isalpha()

    # ----------------------------------------
    #               MAIN STATE
    # ----------------------------------------

    def build_string(self, char):
        # ----------------------------------------
        #             SPACE SUBSTATE
        # ----------------------------------------

        if self.to_ascii(char) <= 32:
            # If current token exists, we append it
            if self.curr_token:
                if self.to_upper(self.curr_val) in self.KEYWORDS:
                    self.curr_token = self.lookup(
                        self.KEYWORDS, self.to_upper(self.curr_val))
                    self.tokens.append((self.curr_token, self.to_lower(
                        self.curr_val), self.curr_row, self.curr_col - 1))
                    self.metadata.append({'TOKEN': self.curr_token, 'VALUE': self.to_lower(
                        self.curr_val), 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''
                    return

                if self.to_upper(self.curr_val) in self.OPERATORS:
                    self.curr_token = self.lookup(
                        self.OPERATORS, self.to_upper(self.curr_val))
                    self.tokens.append((self.curr_token, self.to_lower(
                        self.curr_val), self.curr_row, self.curr_col - 1))
                    self.metadata.append({'TOKEN': self.curr_token, 'VALUE': self.to_lower(
                        self.curr_val), 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''
                    return

                if self.to_upper(self.curr_val) in self.SYSTEM:
                    self.curr_token = self.lookup(
                        self.SYSTEM, self.to_upper(self.curr_val))
                    self.tokens.append((self.curr_token, self.to_lower(
                        self.curr_val), self.curr_row, self.curr_col - 1))
                    self.metadata.append({'TOKEN': self.curr_token, 'VALUE': self.to_lower(
                        self.curr_val), 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''
                    return

                # Current token value is not in any table
                if self.to_upper(self.curr_val) not in self.OPERATORS:
                    if self.to_upper(self.curr_val) not in self.KEYWORDS:
                        if self.curr_token == 'TK_COLON':
                            self.tokens.append(
                                (self.curr_token, ':', self.curr_row, self.curr_col - 1))
                            self.metadata.append(
                                {'TOKEN': self.curr_token, 'VALUE': ':', 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                            self.curr_token = ''
                            self.curr_val = ''
                        elif self.curr_token == 'TK_OPEN_PARENTHESIS':
                            self.tokens.append(
                                (self.curr_token, '(', self.curr_row, self.curr_col - 1))
                            self.metadata.append(
                                {'TOKEN': self.curr_token, 'VALUE': '(', 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                            self.curr_token = ''
                            self.curr_val = ''
                        else:
                            self.tokens.append((self.curr_token, self.to_lower(
                                self.curr_val), self.curr_row, self.curr_col - 1))
                            self.metadata.append({'TOKEN': self.curr_token, 'VALUE': self.to_lower(
                                self.curr_val), 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                            self.curr_token = ''
                            self.curr_val = ''
                            return

            # If there is no token and we are looking at spaces, just return
            if not self.curr_token:
                return

        # ----------------------------------------
        #           SEMICOLON SUBSTATE
        # ----------------------------------------

        # Character is a semicolon
        if self.to_ascii(char) == 59 and not self.numeric:
            # If current token exists, we append it
            if self.curr_token:
                # If current token value is a keyword....
                if self.to_upper(self.curr_val) in self.KEYWORDS:
                    self.curr_token = self.lookup(
                        self.KEYWORDS, self.to_upper(self.curr_val))
                    self.tokens.append((self.curr_token, self.to_lower(
                        self.curr_val), self.curr_row, self.curr_col - 1))
                    self.metadata.append({'TOKEN': self.curr_token, 'VALUE': self.to_lower(
                        self.curr_val), 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''

                # If current token is not a keyword...
                # It is currently treated as an identifier
                else:
                    self.tokens.append((self.curr_token, self.to_lower(
                        self.curr_val), self.curr_row, self.curr_col - 1))
                    self.metadata.append({'TOKEN': self.curr_token, 'VALUE': self.to_lower(
                        self.curr_val), 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''

            # If there is no current token, push semicolon token
            if not self.curr_token:
                self.tokens.append(
                    ('TK_SEMICOLON', ';', self.curr_row, self.curr_col))
                self.metadata.append(
                    {'TOKEN': 'TK_SEMICOLON', 'VALUE': ';', 'ROW': self.curr_row, 'COL': self.curr_col})
                return

        # ----------------------------------------
        #           LESS THAN SUBSTATE
        # ----------------------------------------

        # Character is <
        if self.to_ascii(char) == 60:
            if not self.curr_token:
                self.curr_token = 'TK_LESS'

        # ----------------------------------------
        #           GREATER THAN SUBSTATE
        # ----------------------------------------

        # Character is >
        if self.to_ascii(char) == 62:
            if not self.curr_token:
                self.curr_token = 'TK_GREATER'

        # ----------------------------------------
        #           EXCLAMATION SUBSTATE
        # ----------------------------------------

        # Character is !
        if self.to_ascii(char) == 33:
            if not self.curr_token:
                self.curr_token = 'TK_EXCLAMATION'

        # ----------------------------------------
        #             COLON SUBSTATE
        # ----------------------------------------

        # Character is colon
        if self.to_ascii(char) == 58:
            # If there is no current token, assign colon token
            if not self.curr_token:
                self.curr_token = 'TK_COLON'
                return

        # ----------------------------------------
        #             EQUALS SUBSTATE
        # ----------------------------------------

        # Character is equals
        if self.to_ascii(char) == 61:
            # If there is no current token, push equals token
            if not self.curr_token:
                self.tokens.append(
                    ('TK_EQUALS', '=', self.curr_row, self.curr_col))
                self.metadata.append(
                    {'TOKEN': 'TK_EQUALS', 'VALUE': '=', 'ROW': self.curr_row, 'COL': self.curr_col})
                self.curr_token = ''
                return

            # If there is a current token, it can either be a colon, less than, or greater than
            if self.curr_token == 'TK_COLON':
                self.tokens.append(
                    ('TK_ASSIGNMENT', ':=', self.curr_row, self.curr_col - 1))
                self.metadata.append(
                    {'TOKEN': 'TK_ASSIGNMENT', 'VALUE': ':=', 'ROW': self.curr_row, 'COL': self.curr_col - 1})
                self.curr_token = ''
                return

        # ----------------------------------------
        #              DOT SUBSTATE
        # ----------------------------------------

        # Character is a dot
        if self.to_ascii(char) == 46:
            # If there is a current token, it is END
            if self.curr_token:
                self.tokens.append(
                    ('TK_END_CODE', 'end.', self.curr_row, self.curr_col))
                self.metadata.append(
                    {'TOKEN': 'TK_END_CODE', 'VALUE': 'end.', 'ROW': self.curr_row, 'COL': self.curr_col})
                self.curr_token = ''
                return

        # ----------------------------------------
        #              COMMA SUBSTATE
        # ----------------------------------------

        # Character is a comma
        if self.to_ascii(char) == 44:
            self.tokens.append(('TK_COMMA', ',', self.curr_row, self.curr_col))
            self.metadata.append(
                {'TOKEN': 'TK_COMMA', 'VALUE': ',', 'ROW': self.curr_row, 'COL': self.curr_col})
            self.curr_token = ''
            return

        # ----------------------------------------
        #       OPEN PARENTHESIS SUBSTATE
        # ----------------------------------------

        # Character is left parenthesis
        if self.to_ascii(char) == 40:
            if self.curr_token:
                self.tokens.append(
                    ('TK_OPEN_PARENTHESIS', '(', self.curr_row, self.curr_col - 1))
                self.metadata.append(
                    {'TOKEN': 'TK_OPEN_PARENTHESIS', 'VALUE': '(', 'ROW': self.curr_row, 'COL': self.curr_col})
                self.curr_token = ''

            # Possible to be start of comment, store token
            if not self.curr_token:
                self.curr_token = 'TK_OPEN_PARENTHESIS'
                return

        # ----------------------------------------
        #              MULT SUBSTATE
        # ----------------------------------------

        # Character is *
        if self.to_ascii(char) == 42:
            # If there is no current token, push * token
            if not self.curr_token:
                self.tokens.append(
                    ('TK_MULT', '*', self.curr_row, self.curr_col))
                self.metadata.append(
                    {'TOKEN': 'TK_MULT', 'VALUE': '*', 'ROW': self.curr_row, 'COL': self.curr_col})
                return

            # If there is a current token, it must form (*
            if self.curr_token:
                self.tokens.append(
                    ('TK_BEGIN_COMMENT', '(*', self.curr_row, self.curr_col))
                self.metadata.append(
                    {'TOKEN': 'TK_BEGIN_COMMENT', 'VALUE': '(*', 'ROW': self.curr_row, 'COL': self.curr_col})
                self.curr_token = ''
                self.comment = True
                return

        # ----------------------------------------
        #        CLOSE PARENTHESIS SUBSTATE
        # ----------------------------------------

        # Character is right parenthesis
        if self.to_ascii(char) == 41:
            # We are not handling a comment, so push token
            self.tokens.append(('TK_CLOSE_PARENTHESIS', ')',
                               self.curr_row, self.curr_col))
            self.metadata.append({'TOKEN': 'TK_CLOSE_PARENTHESIS', 'VALUE': ')',
                                 'ROW': self.curr_row, 'COL': self.curr_col})
            self.curr_val = ''
            return

        # ----------------------------------------
        #               OPEN BRACKET
        # ----------------------------------------

        # Character is [
        if self.to_ascii(char) == 91:
            self.tokens.append(
                ('TK_OPEN_BRACKET', '[', self.curr_row, self.curr_col))
            self.metadata.append(
                {'TOKEN': 'TK_OPEN_BRACKET', 'VALUE': '[', 'ROW': self.curr_row, 'COL': self.curr_col})
            self.curr_val = ''
            return

        # ----------------------------------------
        #               CLOSE BRACKET
        # ----------------------------------------

        # Character is [
        if self.to_ascii(char) == 93:
            self.tokens.append(
                ('TK_CLOSE_BRACKET', ']', self.curr_row, self.curr_col))
            self.metadata.append(
                {'TOKEN': 'TK_CLOSE_BRACKET', 'VALUE': ']', 'ROW': self.curr_row, 'COL': self.curr_col})
            self.curr_val = ''
            return

        # ----------------------------------------
        #           BEGIN QUOTE SUBSTATE
        # ----------------------------------------

        # Character is ' (open quote)
        if self.to_ascii(char) == 39:
            self.string = True
            self.curr_val += char
            return

        # ----------------------------------------
        #       BEGIN DIGIT STRING SUBSTATE
        # ----------------------------------------

        # Character is a digit
        if self.handle_numeric(char):
            self.numeric = True
            self.curr_val += char
            return

        # ----------------------------------------
        #              PLUS SUBSTATE
        # ----------------------------------------

        # Character is plus
        if self.to_ascii(char) == 43:
            self.tokens.append(('TK_PLUS', '+', self.curr_row, self.curr_col))
            self.metadata.append(
                {'TOKEN': 'TK_PLUS', 'VALUE': '+', 'ROW': self.curr_row, 'COL': self.curr_col})
            self.curr_val = ''
            return

        # ----------------------------------------
        #              TILDA SUBSTATE
        # ----------------------------------------

        # Character is a ~
        if self.to_ascii(char) == 126:
            self.tokens.append(('TK_RANGE', '~', self.curr_row, self.curr_col))
            self.metadata.append(
                {'TOKEN': 'TK_RANGE', 'VALUE': '~', 'ROW': self.curr_row, 'COL': self.curr_col})
            self.curr_val = ''
            return

        # ----------------------------------------
        #            MINUS SUBSTATE
        # ----------------------------------------

        # Character is minus
        if self.to_ascii(char) == 45:
            self.tokens.append(('TK_MINUS', '-', self.curr_row, self.curr_col))
            self.metadata.append(
                {'TOKEN': 'TK_MINUS', 'VALUE': '-', 'ROW': self.curr_row, 'COL': self.curr_col})
            self.curr_val = ''
            return

        # ----------------------------------------
        #              DIV SUBSTATE
        # ----------------------------------------

        # Character is /
        if self.to_ascii(char) == 47:
            self.tokens.append(
                ('TK_DIV_FLOAT', '/', self.curr_row, self.curr_col))
            self.metadata.append(
                {'TOKEN': 'TK_DIV_FLOAT', 'VALUE': '/', 'ROW': self.curr_row, 'COL': self.curr_col})
            self.curr_val = ''
            return

        # ----------------------------------------
        #          IDENTIFIER SUBSTATE
        # ----------------------------------------

        # If none of the above cases are true, build string
        self.curr_val += char
        # string is not in either table
        if self.to_upper(self.curr_val) not in self.KEYWORDS:
            if self.to_upper(self.curr_val) not in self.OPERATORS:
                if self.to_upper(self.curr_val) not in self.SYSTEM:
                    self.curr_token = 'TK_IDENTIFIER'

    # ----------------------------------------
    #               TABLES
    # ----------------------------------------

    KEYWORDS = {
        'BEGIN': 'TK_BEGIN',
        'BREAK': 'TK_BREAK',
        'CONST': 'TK_CONST',
        'DO': 'TK_DO',
        'DOWNTO': 'TK_DOWNTO',
        'ELSE': 'TK_ELSE',
        'END': 'TK_END',
        'END.': 'TK_END_CODE',
        'FOR': 'TK_FOR',
        'FUNCTION': 'TK_FUNCTION',
        'IDENTIFIER': 'TK_IDENTIFIER',
        'IF': 'TK_IF',
        'LABEL': 'TK_LABEL',
        'PROGRAM': 'TK_PROGRAM',
        'REPEAT': 'TK_REPEAT',
        'STRING': 'TK_STRING',
        'THEN': 'TK_THEN',
        'TO': 'TK_TO',
        'TYPE': 'TK_TYPE',
        'VAR': 'TK_VAR',
        'UNTIL': 'TK_UNTIL',
        'WHILE': 'TK_WHILE',
        'INTEGER': 'TK_ID_INTEGER',
        'REAL': 'TK_ID_REAL',
        'CHAR': 'TK_ID_CHAR',
        'BOOLEAN': 'TK_ID_BOOLEAN',
        'OF': 'TK_OF'
    }

    OPERATORS = {
        '+': 'TK_PLUS',
        '-': 'TK_MINUS',
        '*': 'TK_MULT',
        '/': 'TK_DIV_FLOAT',
        'DIV': 'TK_DIV',
        'MOD': 'TK_MOD',
        ':': 'TK_COLON',
        '=': 'TK_EQUALS',
        ':=': 'TK_ASSIGNMENT',
        '>': 'TK_GREATER',
        '<': 'TK_LESS',
        '>=': 'TK_GREATER_EQUALS',
        '<=': 'TK_LESS_EQUALS',
        '!': 'TK_EXCLAMATION',
        '!=': 'TK_NOT_EQUALS',
        'AND': 'TK_AND',
        'XOR': 'TK_XOR',
        'OR': 'TK_OR',
        'NOT': 'TK_NOT',
        ';': 'TK_SEMICOLON',
        '(': 'TK_OPEN_PARENTHESIS',
        ')': 'TK_CLOSE_PARENTHESIS',
        '\'': 'TK_QUOTE',
        '(*': 'TK_BEGIN_COMMENT',
        '*)': 'TK_END_COMMENT',
        ',': 'TK_COMMA',
        '~': 'TK_RANGE',
        'ARRAY': 'TK_ARRAY',
        '[': 'TK_OPEN_BRACKET',
        ']': 'TK_CLOSE_BRACKET',
        '\'': 'TK_APOSTROPHE',
    }

    SYSTEM = {
        'WRITELN': 'TK_WRITELN',
        'ABS': 'TK_ABS'
    }
