import os
import re

class Parser():
    def __init__(self, data_dir="data"):
        self.__data_dir = data_dir
        self.__nodes = {}
        self.__read_data()

    def __read_data(self, data_dir = None):
        if not data_dir:
            data_dir = self.__data_dir
        print ("reading from data dir", data_dir)
        with os.scandir(data_dir) as it:
            for entry in it:
                if not entry.name.startswith('.'):
                    if entry.is_file():
                        self.__add_node(data_dir, entry.name)
                    else:
                        self.__read_data(os.path.join(data_dir, entry.name))

    def __add_node(self, data_dir, name):
        fname = os.path.join(data_dir, name)
        print ("reading", fname)
        m = re.search('(\d+)_(.*)', name)
        if not m:
            raise RuntimeError("Invalid data file name: %s" % name)

        nid = int(m.group(1))
        print ("New node", nid)

        node = {
                'id': nid,
                'file': fname,
                'text': [],
                'pre': [],
                'post': []
                }
        
        if nid in self.__nodes:
            print ("Duplicate ids found", node['file'], "and", self.__nodes[nid]['file'])
            raise RuntimeError("Duplicate data file ids")

        # Data file parsing
        with open(fname, 'r') as f:
            state = 0
            for line in f:
                if line[0] == '#':
                    continue
                elif line[0] != ';':
                    if state == 2:
                        raise RuntimeError("Text after post-code in %s" % fname)

                    node['text'].append(line[:-1])

                    state = 1
                else:
                    if state == 0:
                        node['pre'].append(line[1:-1])
                    else:
                        node['post'].append(line[1:-1])
                        state = 2

        self.__nodes[nid] = node

    @property
    def nodes(self):
        return self.__nodes
