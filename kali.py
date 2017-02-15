# Käyttö liittymä

import curses

class Kali:
    def __init__(self):
        self.scr = curses.initscr()
        height,width = self.scr.getmaxyx()
        if height < 24 or width < 80:
            raise RuntimeError("Terminal size must be at least 80x24")
        curses.noecho()
        self.scr.keypad(True)
        curses.cbreak()

    def __del__(self):
        curses.nocbreak()
        self.scr.keypad(False)
        curses.echo()
        curses.endwin()

    def clear(self):
        self.row = 0

        self.scr.clear()
        self.scr.refresh()

    def wait_enter(self):
        while True:
            c = self.scr.getch()
            if c == ord('\n'):
                return

    def output(self, text):
        if isinstance(text, list):
            for line in text:
                self.scr.addstr(self.row, 0, line)
                self.row += 1
        else:
            self.scr.addstr(self.row, 0, text)
            self.row += 1
        self.scr.refresh()
