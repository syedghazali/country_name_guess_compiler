import sys

# --- TOKEN TYPES ---
# These are the "labels" we give to words in your code
TOK_GAME    = 'GAME'
TOK_LIVES   = 'MAX_LIVES'
TOK_LEVEL   = 'LEVEL'
TOK_TARGET  = 'TARGET'
TOK_HINT    = 'HINT'
TOK_SOLVE   = 'SOLVE'
TOK_STRING  = 'STRING'
TOK_INT     = 'INT'
TOK_SEMI    = 'SEMICOLON'
TOK_EOF     = 'EOF'

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()

    def make_string(self):
        string_val = ''
        self.advance() # skip opening quote
        while self.current_char is not None and self.current_char != '"':
            string_val += self.current_char
            self.advance()
        self.advance() # skip closing quote
        return Token(TOK_STRING, string_val)

    def make_number(self):
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token(TOK_INT, int(num_str))

    def make_identifier(self):
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()

        # Check if the word is a special keyword
        if id_str == 'GAME': return Token(TOK_GAME, id_str)
        elif id_str == 'MAX_LIVES': return Token(TOK_LIVES, id_str)
        elif id_str == 'LEVEL': return Token(TOK_LEVEL, id_str)
        elif id_str == 'TARGET': return Token(TOK_TARGET, id_str)
        elif id_str == 'HINT': return Token(TOK_HINT, id_str)
        elif id_str == 'SOLVE': return Token(TOK_SOLVE, id_str)
        else:
            # If it's not a keyword, it's an error in this specific language design
            raise Exception(f"Unknown Keyword: {id_str}")

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char == '/' and self.text[self.pos+1:self.pos+2] == '/':
                self.skip_comment()
                continue

            if self.current_char.isalpha():
                return self.make_identifier()

            if self.current_char == '"':
                return self.make_string()

            if self.current_char.isdigit():
                return self.make_number()

            if self.current_char == ';':
                self.advance()
                return Token(TOK_SEMI, ';')

            raise Exception(f"Illegal Character: {self.current_char}")

        return Token(TOK_EOF, None)