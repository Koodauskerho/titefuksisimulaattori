# Käyttö liittymä

import curses
from curses.textpad import rectangle

class Kali:
    def __init__(self):
        self.scr = curses.initscr()
        height,width = self.scr.getmaxyx()
        if height < 24 or width < 80:
            raise RuntimeError("Terminal size must be at least 80x24")
        curses.noecho()
        self.scr.keypad(True)
        curses.cbreak()
        curses.curs_set(False)

        self.buf = []

    def __del__(self):
        curses.nocbreak()
        self.scr.keypad(False)
        curses.echo()
        curses.endwin()

    def __redraw(self):
        buf = self.buf
        self.clear()
        self.output(buf)

    def askchoice(self, choices):
        for i, c in enumerate(choices):
            self.scr.addstr(self.row+1+i, 2, "%s) %s" % (c[0].upper(), c[1]))
        self.scr.refresh()
        while True:
            ch = self.scr.getch()
            for i, c in enumerate(choices):
                if ch == ord(c[0]):
                    self.__redraw()
                    return i

    def box(self, r1, c1, h, w):
        for i in range(w-2):
            self.scr.addch(r1, c1+1+i, "═")
        for i in range(w-2):
            self.scr.addch(r1+h-1, c1+1+i, "═")
        for i in range(h-2):
            self.scr.addch(r1+1+i, c1, "║")
            self.scr.addch(r1+1+i, c1+w-1, "║")
        self.scr.addch(r1, c1, "╔")
        self.scr.addch(r1, c1+w-1, "╗")
        self.scr.addch(r1+h-1, c1, "╚")
        self.scr.addch(r1+h-1, c1+w-1, "╝")

    def clear(self):
        self.row = 0
        del self.buf[:]

        self.scr.clear()
        self.scr.refresh()

    def output(self, text):
        if isinstance(text, str):
            text = text.split("\n")

        for line in text:
            self.scr.addstr(self.row, 0, line)
            self.buf.append(line)
            self.row += 1
        self.scr.refresh()

    def prompt(self, text, default=""):
        if isinstance(text, str):
            text = text.split("\n")

        maxlen = 0
        for line in text:
            if len(line) > maxlen:
                maxlen = len(line)

        x1 = 40 - maxlen//2 - 2
        self.scr.clear()
        self.box(1, x1, 6+len(text), maxlen+4)
        for i in range(len(text)):
            rivi = text[i]
            rx = 40 - len(rivi)//2
            self.scr.addstr(3+i, rx, rivi)

        self.scr.addstr(4+len(text), x1+2, " "*maxlen, curses.A_REVERSE)

        ret = default
        self.scr.addstr(4+len(text), x1+2, ret[-maxlen:] + " "*(maxlen-len(ret)), curses.A_REVERSE)
        self.scr.refresh()

        while True:
            c = self.scr.getch()
            if c == 127:
                ret = ret[:-1]
            elif c == ord('\n'):
                if len(ret) > 0:
                    break
            else:
                ret += chr(c)
            self.scr.addstr(4+len(text), x1+2, ret[-maxlen:] + " "*(maxlen-len(ret)), curses.A_REVERSE)
            self.scr.refresh()

        # redraw buffer
        self.__redraw()

        return ret

    def wait_enter(self):
        while True:
            c = self.scr.getch()
            if c == ord('\n'):
                return
