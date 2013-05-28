from collections import deque
import numpy as np

from Body import Body

class ReaderError(Exception):
    pass

class Reader(object):
    def __init__(self, start_file):
        self.file = open(start_file, 'r')
        self.bodies = []
        self.lines = deque(self.file.readlines())
        
    def getBodies(self):
        while len(self.lines) > 0:
            try:
                body = self._readOne()
                self.bodies.append(body)
            except IndexError:
                pass
        return self.bodies
        
    def _readOne(self):

        # read the initial line containing the name of the body
        name = None
        while name is None:
            line = self.lines.popleft()
            # catch the end of line (an empty line, w/o whitespace...)
            if len(line) == 0:
                return None
            else:
                line = line.strip()

            if line.endswith('{'):
                name = line[:-1]
            elif len(line) != 0:
                name = line

        # now, find the opening curly bracket
        while '{' not in line:
            line = self.lines.popleft().strip()
            # if we find text between the name and the curly brackets, 
            # somebody goofed
            if len(line) != 0 and '{' not in line:
                raise ReaderError('Incorrect body config: %s' %line)

        props = np.zeros(10)
        i = 0
        while '}' not in line:
            line = self.lines.popleft().strip()

            if len(line) == 0 or '{' in line:
                raise ReaderError('Unterminated body!')
            if '}' in line:
                break

            line = line.split(',')
            for num in line:
                props[i] = float(num)
                i += 1
            
        return Body(*props)
