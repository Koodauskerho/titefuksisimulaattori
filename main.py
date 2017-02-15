#!/usr/bin/env python3

import os

from parser import Parser
from game import Game

def main():
    p = Parser()
    g = Game(p.nodes)
    try:
        g.start()
    except:
        g.stop()
        raise

if __name__ == '__main__':
    main()
