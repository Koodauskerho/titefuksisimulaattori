from kali import Kali

class Game():
    def __init__(self, nodes):
        self.__nodes = nodes
        self.__vars = {
                'next': self.__next,
                'lose': self.__lose,
                'print': self.__print,
                'prompt': self.__prompt,
                'wait': self.__wait,
                }
        self.__node = self.__nodes[0]
        self.__nextid = -1

    def __lose(self, msg="HÄVISIT PELIN!"):
        self.__kali.clear()
        self.__kali.output(msg)
        self.__kali.wait_enter()
        raise RuntimeError("Player skill too low")

    def __next(self, nid):
        self.__nextid = nid

    def __print(self, text):
        self.__kali.output(str(text))

    def __prompt(self, text):
        return self.__kali.prompt(text)

    def __wait(self):
        self.__kali.wait_enter()
    
    def start(self):
        print ("Starting game")
        self.__kali = Kali()
        while True:
            self.__nextid = -1
            node = self.__node

            self.__kali.clear()

            for block in node["data"]:
                if block["type"] == "code":
                    code = "\n".join(block["data"])
                    exec(code, self.__vars)
                elif block["type"] == "text":
                    self.__kali.output(block["data"])

            if not self.__nextid in self.__nodes:
                self.__kali.output("ERROR: Tried going to invalid index %" % self.__nextid)
                self.__kali.wait_enter()
                return

            self.__kali.wait_enter()
            self.__node = self.__nodes[self.__nextid]
        self.stop()

    def stop(self):
        del self.__kali
