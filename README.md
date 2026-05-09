
# RetroLogo Turtle Graphics Compiler

## Description
RetroLogo is a compiler construction semester project inspired by the classic LOGO turtle graphics language.

The compiler demonstrates:
- Lexical Analysis
- Syntax Analysis
- Semantic Analysis
- Intermediate Code Generation
- Optimization
- Code Generation

---

## Features

- Turtle graphics rendering
- Variables and arithmetic expressions
- REPEAT loops
- Circle drawing
- Pen controls
- Debug mode
- Interactive mode
- IR generation
- Optimization support

---

## Installation

Install Python 3 with Tk support (required for the turtle graphics window).

Clone repository:

git clone https://github.com/retro-logo/compiler.git

---

## Running Programs

python src/compiler.py tests/square.rlogo

(Run from the project root. The compiler adjusts sys.path automatically.)

---

## Debug Mode

python src/compiler.py tests/square.rlogo --debug

---

## Interactive Mode

python src/compiler.py --interactive

---

## Folder Structure

src/ -> Compiler source files
tests/ -> Sample RetroLogo programs
docs/ -> Documentation
handwritten_guides/ -> Hardcopy preparation guides

---

## Compiler Phases

1. Lexer
2. Parser
3. Semantic Analyzer
4. IR Generator
5. Optimizer
6. Code Generator
