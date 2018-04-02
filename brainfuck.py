#!/usr/bin/python
#
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
#
# Usage: ./brainfuck.py [FILE]

import sys
import getch

def execute(filename):
  """[summary]
  Loads the source code from the file and delivers it to the parser.

  Arguments:
    filename {[str]} -- [path of the brainfuck source code]
  """

  f = open(filename, "r")
  evaluate(f.read())
  f.close()


def evaluate(code):
  """[summary]
  This function is the parser for the brainfuck code.

  Arguments:
    code {[str]} -- [source code (not analysed)]
  """

  code     = cleanup(list(code))
  bracemap = buildbracemap(code)

  cells, codeptr, cellptr = [0], 0, 0

  while codeptr < len(code):
    command = code[codeptr]

    if command == ">":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "<":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "+":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "-":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
    if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
    if command == ".": sys.stdout.write(chr(cells[cellptr]))
    if command == ",": cells[cellptr] = ord(getch.getch())
      
    codeptr += 1


def cleanup(code):
  """[summary]
  Simple scanner for the brainfuck source code.
  
  Arguments:
    code {[str]} -- [source code]
  
  Returns:
    [str] -- [analysed code]
  """

  return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))


def buildbracemap(code):
  """[summary]
  Generates a map for the start and end addresses of the loops.
  
  Arguments:
    code {[str]} -- [analysed code]
  
  Returns:
    [dictionary] -- [simple map for the loops.]
  """

  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


def main():
  """[summary]
  simple main program
  """

  if len(sys.argv) == 2: execute(sys.argv[1])
  else: print("Usage:", sys.argv[0], "filename")

if __name__ == "__main__": main()

