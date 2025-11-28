from lexer import Lexer
from compiler import Compiler
import sys

def main():
    # 1. Open the source code file
    try:
        with open('game.cgs', 'r') as file:
            source_code = file.read()
    except FileNotFoundError:
        print("Error: Could not find 'game.cgs' file.")
        return

    # Show a small help if user passes -h
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print('Usage: python main.py [gui]')
        print('  gui  - launch the Tkinter GUI')
        return

    # 2. Initialize Lexer (Phase 1)
    lexer = Lexer(source_code)

    # 3. Initialize Compiler/Parser (Phase 2 & Execution)
    compiler = Compiler(lexer)

    # 4. Allow either CLI flow (default) or GUI if user passed 'gui'
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'gui':
        # Lazy-load tkinter-based GUI to keep CLI usage lightweight
        try:
            from gui import GameGUI
            import tkinter as tk
            root = tk.Tk()
            app = GameGUI(root)
            app.reset_state_from_file()
            root.mainloop()
            return
        except Exception as e:
            print(f"Failed to start GUI: {e}")
            print("Falling back to CLI mode...")

    # CLI mode: run the compiler and execute the program using the CLI interactive loop
    print("Starting Compiler (CLI mode)...")
    try:
        compiler.run(execute_on_solve=True)
        print("\n--- Program Finished Successfully ---")
    except Exception as e:
        print(f"\nCompiler Error: {e}")

if __name__ == "__main__":
    main()