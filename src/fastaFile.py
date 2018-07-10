
import re

#simple class to read fasta formated file and lookup sequences by identifier
class FastaFile:
    def __init__(self, fname):
        self.fname = fname
        self._sequences = dict()
        self.read()

    def read(self):
        inF = open(self.fname, 'rU')
        lines = inF.readlines()

        for i, line in enumerate(lines):
            if re.match('^\>[a-z]+\|\w+\|', line):
                elems = line.split('|')
                assert(len(elems) >= 3)
                id = elems[1]
                self._sequences[id] = lines[i + 1].strip()

    def getSequence(self, id):
        if id not in self._sequences:
            raise RuntimeError('{} not found in fasta file'.format(id))
        return self._sequences[id]

