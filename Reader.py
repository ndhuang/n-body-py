import numpy as np

class ReaderError(Exception):
    pass

class Reader(object):
    def __init__(self, start_file):
        self.file = open(start_file, 'r')
        self.bodies = []
        
    def get_bodies(self):
        while True:
            try:
                self.bodies.append(self._read_one)
            except ReaderError:
                return self.bodies
        
    def _read_one(self):
        line = self.file.readline().strip()
        if line.endswith('{'):
            name = line[:-1])
        else:
            name = line
        
        props = np.zeros(10)
        i = 0
        while '}' not in line:
            line = self.file.readline().strip()

            if len(line) == 0 or '{' in line:
                raise ReaderError('Untermintaed body!')

            line = line.split('.')
            for num in line:
                props[i] = float(num)
                i += 1
            
        return Body(*props)
