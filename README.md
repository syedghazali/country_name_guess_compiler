# CountryGuessCompiler - Cute Tkinter UI

This project is a tiny DSL-driven country guessing game. It includes:

- `lexer.py` - tokenizes the DSL.
- `compiler.py` - parses and stores game state levels.
- `main.py` - entry point that can launch CLI or a cute Tkinter GUI.
- `gui.py` - Tkinter-based UI that reads `game.cgs`, shows hints and lives, and handles guesses.
- `game.cgs` - a sample game script.

## Run

Open a terminal in the project folder and run one of the following commands with Python 3:

- CLI mode (default):

```powershell
python main.py
```

- GUI mode (cute UI with Tkinter):
### Features

- Cute pastel-themed GUI with friendly fonts and emojis.
- Support for multiple levels defined in `game.cgs` (the GUI progresses automatically on correct guesses).
- `Reset` button reloads `game.cgs` to reflect changes during development.
- `Enter` key to submit, `Exit` to close the game.

### Notes

- Ensure `game.cgs` is in the same directory as the scripts. The GUI will parse it and create levels accordingly.
- Tkinter is part of standard Python distribution on Windows; no extra packages required.


```powershell
python main.py gui
```

If you edit `game.cgs`, the GUI will load the new levels and configuration on Reset.

Enjoy the cute UI! 🐣🎨
"# country_name_guess_compiler" 
