import crc
import zlib
import pybin

chunk_ids = ['','IHDR','IDAT','IEND','bKGD','tRNS','PLTE','tEXT', 'gAMA']

class Chunk:
    """Container class for png file chunks."""

    _name = ''
    _data = []

    # methods

    def _calc_crc(self):
        """Calculate the chunk crc."""

        bytefield = []

        # checksum runs over chunk name and data, so append chunk name first
        for c in self._name:
            bytefield.append(pybin.ctoi(c))

        # append data
        bytefield += self._data

        # calculate checksum and return
        return crc.crc32(bytefield)



    def set_name(self,name):
        """Sets chunk name to a four character identifier."""

        # is name a known chunk identifier??
        if not name in chunk_ids:
            return True

        # set chunk name and return
        self._name = name
        return False



    def append(self, value, n = 1):
        """Appends value in network order to end of chunk within given bytes."""

        # store lower 8 bytes on a stack n times (last bytes may be 0)
        i = value
        stack = []
        for k in range(n):
            stack.append(value % 256)
            value /= 256

        # pop bytes off of stack and onto chunk
        for k in range(n):
            self._data.append(stack.pop())

    def pop(self, n):
        """Gets the top n bytes from chunk and puts them into an int."""
        

    def convert(self, binarydata = None):
        """Return chunk data as a string."""

        # get length and name fields
        output = ''
        output += pybin.iton(len(self._data))
        output += self._name

        # append data field
        if binarydata != None:
            output += binarydata
        else:
            for i in self._data:
                output += pybin.itoc(i)

        # append checksum and return
        output += pybin.iton(self._calc_crc())
        return output



    def compress(self):
        """Return chunk string with DEFLATEd data field."""

        data = ''
        for i in self._data:
            data += pybin.itoc(i)

        data = zlib.compress(data)

        # compress data in chunk array (to aid checksum)
        self._data = []
        for c in data:
            self._data.append(pybin.ctoi(c))
        
        # return converted to string
        return self.convert(data)    



    def __init__(self, name = '', data = []):
        """Constructor defaults to empty with no name."""
        self.set_name(name)
        self._data = data



    def read(self, string):
        
        if not isinstance(string,str):
            return self
        
        # chunk data is length between chunk name and crc
        l = len(str) - 8
        
        # first 4 bytes are chunk name
        self.set_name( contents[:4] )
        
        # discard chunk name and crc (4 bytes each) for chunk data
        contents = string[4:-4]
        
        # last 4 bytes are crc
        crc = pybin.ntoi(string[-4:])
        
        # convert that data from binary to ints
        self._data = []
        for c in contents:
            self._data.append(pybin.ctoi(c))
        
        # check chunk integrity
        if chunk.calc_crc() != crc:
            print 'Corrupted chunk'
            return None
        
        # chunk is initialized and clean
        return self

