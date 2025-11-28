from lexer import *

class Compiler:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        
        # Symbol Table (Variables to store game state)
        self.game_title = ""
        self.max_lives = 1
        self.current_target = ""
        self.current_hint = ""
        # Levels support: store a list of level dicts {level, target, hint}
        self.levels = []
        self.current_level_num = None

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Syntax Error: Expected {token_type}, got {self.current_token.type}")

    def run(self, execute_on_solve=False):
        """
        Parse the entire input. If execute_on_solve is True, the compiler will run
        runtime behavior on encountering the SOLVE token (backward compatible with CLI).
        Otherwise it will only parse and populate symbol table state for the UI to consume.
        """
        # Grammar: Program -> Statement*
        while self.current_token.type != TOK_EOF:
            self.statement(execute_on_solve=execute_on_solve)

    def statement(self, execute_on_solve=False):
        # Grammar: Statement -> (GAME | MAX_LIVES | LEVEL | TARGET | HINT | SOLVE) Value SEMI
        
        if self.current_token.type == TOK_GAME:
            self.eat(TOK_GAME)
            self.game_title = self.current_token.value
            self.eat(TOK_STRING)
            self.eat(TOK_SEMI)
            print(f"--- Welcome to: {self.game_title} ---")

        elif self.current_token.type == TOK_LIVES:
            self.eat(TOK_LIVES)
            self.max_lives = self.current_token.value
            self.eat(TOK_INT)
            self.eat(TOK_SEMI)
            print(f"System: Lives set to {self.max_lives}")

        elif self.current_token.type == TOK_LEVEL:
            self.eat(TOK_LEVEL)
            lvl = self.current_token.value
            self.eat(TOK_INT)
            self.eat(TOK_SEMI)
            # Register a new level entry; subsequent TARGET and HINT will fill it.
            self.current_level_num = lvl
            self.levels.append({'level': lvl, 'target': None, 'hint': None})
            print(f"\n[LOADING LEVEL {lvl}]")

        elif self.current_token.type == TOK_TARGET:
            self.eat(TOK_TARGET)
            self.current_target = self.current_token.value
            self.eat(TOK_STRING)
            self.eat(TOK_SEMI)
            # If we have a current level, write the target into it.
            if self.current_level_num is not None:
                self.levels[-1]['target'] = self.current_target

        elif self.current_token.type == TOK_HINT:
            self.eat(TOK_HINT)
            self.current_hint = self.current_token.value
            self.eat(TOK_STRING)
            self.eat(TOK_SEMI)
            # If we have a current level, write the hint into it.
            if self.current_level_num is not None:
                self.levels[-1]['hint'] = self.current_hint

        elif self.current_token.type == TOK_SOLVE:
            self.eat(TOK_SOLVE)
            self.eat(TOK_SEMI)
            # This signals that the program wants to execute. In CLI mode, execute,
            # but for GUI we will let the GUI handle runtime behavior so skip running
            # execution here unless `execute_on_solve` is True.
            if execute_on_solve:
                self.execute_game_logic()
            
        else:
            raise Exception(f"Unexpected token: {self.current_token}")

    def execute_game_logic(self):
        # This function acts as the runtime environment for your language
        lives = self.max_lives
        won = False
        
        while lives > 0 and not won:
            print(f"HINT: {self.current_hint}")
            print(f"Lives remaining: {lives}")
            guess = input("Enter full country name: ").strip().upper()
            
            if guess == self.current_target.upper():
                print(">>> CORRECT! You passed this level. <<<\n")
                won = True
            else:
                print(">>> WRONG! <<<")
                lives -= 1
        
        if not won:
            print(f"GAME OVER. The answer was {self.current_target}")
            exit()

    def get_state(self):
        """Return the parsed game state for use by UIs.

        Returns a dict with keys: title, max_lives, target, hint
        """
        return {
            'title': self.game_title,
            'max_lives': self.max_lives,
            'target': self.current_target,
            'hint': self.current_hint,
            'levels': self.levels
        }