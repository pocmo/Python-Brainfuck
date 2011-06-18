#!/usr/bin/python
#
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
#
# Usage: ./brainfuck.py [FILE]

import sys
import re
import getch

def execute(filename):
  file     = open(filename, "r")
  code     = cleanup(list(file.read()))
  bracemap = buildbracemap(code)

  cells       = [0]
  codepointer = 0
  cellpointer = 0

  while codepointer < len(code):
    command = code[codepointer]

    if command == ">":
      cellpointer += 1
      if cellpointer == len(cells): cells.append(0)

    if command == "<":
      if cellpointer <= 1: cellpointer = 0
      else: cellpointer -= 1

    if command == "+":
      if cells[cellpointer] < 255:
        cells[cellpointer] += 1
      else:
        cells[cellpointer] = 0

    if command == "-":
      if cells[cellpointer] > 0:
        cells[cellpointer] -= 1
      else:
        cells[cellpointer] = 255

    if command == "[":
      if cells[cellpointer] == 0:
        codepointer = bracemap[codepointer]

    if command == "]":
      if cells[cellpointer] != 0:
        codepointer = bracemap[codepointer]

    if command == ".":
      sys.stdout.write(chr(cells[cellpointer]))

    if command == ",":
      cells[cellpointer] = ord(getch.getch())
      
    codepointer += 1


def cleanup(code):
  return filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code)


def buildbracemap(code):
  temp_bracestack = []
  bracemap        = {}

  for position in range(len(code)):
    command = code[position]
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start

  return bracemap


def main():
  if len(sys.argv) == 2:
    execute(sys.argv[1])
  else:
    print "Usage:", sys.argv[0], "filename"


if __name__ == "__main__":
  main()

