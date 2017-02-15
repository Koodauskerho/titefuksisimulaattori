from kali import Kali

class Game():
    def __init__(self, nodes):
        self.__nodes = nodes
        self.__vars = {
                'next': self.__next,
                'prompt': self.__prompt,
                'lose': self.__lose,
                }
        self.__node = self.__nodes[0]
        self.__nextid = -1

    def __next(self, nid):
        self.__nextid = nid

    def __prompt(self, text):
        pass

    def __lose(self, msg="HÄVISIT PELIN!"):
        self.__kali.clear()
        self.__kali.output(msg)
        self.__kali.wait_enter()
        raise RuntimeError("Player skill too low")
    
    def start(self):
        print ("Starting game")
        self.__kali = Kali()
        while True:
            self.__nextid = -1
            node = self.__node

            self.__kali.clear()
            self.__kali.output(node["file"])

            code = "\n".join(node["pre"])
            exec(code, self.__vars)
            self.__kali.output(node["text"])
            self.__kali.wait_enter()
            code = "\n".join(node["post"])
            exec("\n".join(node["post"]), self.__vars)

            if not self.__nextid in self.__nodes:
                self.__kali.output("ERROR: Tried going to invalid index %" % self.__nextid)
                self.__kali.wait_enter()
                return

            self.__node = self.__nodes[self.__nextid]
        self.stop()

    def stop(self):
        del self.__kali