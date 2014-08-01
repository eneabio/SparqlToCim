import string
import re

class FileReader:
    """ 
    Similar to file class, but allows to access smoothly the lines 
    as when using readlines(), with no memory payload, going back and forth,
    finding regexps and so on.
    """
    def __init__(self,filename, readWrite): # fold>>
        self.__file=file(filename,readWrite)
        self.__currentPos=-1
        # get file length
        self.__file.seek(0,0)
        counter=0
        line=self.__file.readline()
        while line != '':
            counter = counter + 1
            line=self.__file.readline()
        self.__length = counter
        # collect an index of filedescriptor positions against
        # the line number, to enhance search
        self.__file.seek(0,0)
        self.__lineToFseek = []

        while True:
            cur=self.__file.tell()
            line=self.__file.readline()
            # if it's not null the cur is valid for
            # identifying a line, so store
            self.__lineToFseek.append(cur)
            if line == '':
                break
    # <<fold
    def __len__(self): # fold>>
        """
        member function for the operator len()
        returns the file length
        FIXME: better get it once when opening file
        """
        return self.__length
        # <<fold
    def __getitem__(self,key): # fold>>
        """ 
        gives the "key" line. The syntax is

        import FileReader
        f=FileReader.FileReader("a_file")
        line=f[2]

        to get the second line from the file. The internal
        pointer is set to the key line
        """

        mylen = self.__len__()
        if key < 0:
            self.__currentPos = -1
            return ''
        elif key > mylen:
            self.__currentPos = mylen
            return ''

        self.__file.seek(self.__lineToFseek[key],0)
        counter=0
        line = self.__file.readline()
        self.__currentPos = key
        return line
        # <<fold
    def next(self): # fold>>
        if self.isAtEOF():
            raise StopIteration
        return self.readline()
    # <<fold
    def __iter__(self): # fold>>
        return self
    # <<fold
    def readline(self): # fold>>
        """
        read a line forward from the current cursor position.
        returns the line or an empty string when at EOF
        """
        return self.__getitem__(self.__currentPos+1)
        # <<fold
    #Enea
    def writeline(self, line): # fold>>
        """
        read a line forward from the current cursor position.
        returns the line or an empty string when at EOF
        """
        return self.__writeItem__(self.__currentPos, line)
        # <<fold
    def __writeItem__(self,key, line): # fold>>
        """ 
        gives the "key" line. The syntax is

        import FileReader
        f=FileReader.FileReader("a_file")
        line=f[2]

        to get the second line from the file. The internal
        pointer is set to the key line
        """

        mylen = self.__len__()
        if key < 0:
            self.__currentPos = -1
            return ''
        elif key > mylen:
            self.__currentPos = mylen
            return ''

        self.__file.seek(self.__lineToFseek[key],0)
        counter=0
        self.__file.write(line)
        self.__currentPos = key
        return True
        # <<fold    
    def readbackline(self): # fold>>
        """
        read a line backward from the current cursor position.
        returns the line or an empty string when at Beginning of
        file.
        """
        return self.__getitem__(self.__currentPos-1)
        # <<fold
    def currentLine(self): # fold>>
        """
        gives the line at the current cursor position
        """
        return self.__getitem__(self.__currentPos)
        # <<fold
    def currentPos(self): # fold>>
        """ 
        return the current position (line) in the file
        or -1 if the cursor is at the beginning of the file
        or len(self) if it's at the end of file
        """
        return self.__currentPos
        # <<fold
    def toBOF(self): # fold>>
        """
        go to beginning of file
        """
        self.__getitem__(-1)
        # <<fold
    def toEOF(self): # fold>>
        """
        go to end of file
        """
        self.__getitem__(self.__len__())
        # <<fold
    def toPos(self,key): # fold>>
        """
        go to the specified line
        """
        self.__getitem__(key)
        # <<fold
    def isAtEOF(self): # fold>>
        return self.__currentPos == self.__len__()
        # <<fold
    def isAtBOF(self): # fold>>
        return self.__currentPos == -1
        # <<fold
    def isAtPos(self,key): # fold>>
        return self.__currentPos == key
        # <<fold

    def findString(self, thestring, count=1, backward=0): # fold>>
        """
        find the count occurrence of the string str in the file
        and return the line catched. The internal cursor is placed
        at the same line.
        backward is the searching flow.
        For example, to search for the first occurrence of "hello
        starting from the beginning of the file do:

        import FileReader
        f=FileReader.FileReader("a_file")
        f.toBOF()
        f.findString("hello",1,0)

        To search the second occurrence string from the end of the
        file in backward movement do:

        f.toEOF()
        f.findString("hello",2,1)

        to search the first occurrence from a given (or current) position
        say line 150, going forward in the file 

        f.toPos(150)
        f.findString("hello",1,0)

        return the string where the occurrence is found, or an empty string
        if nothing is found. The internal counter is placed at the corresponding
        line number, if the string was found. In other case, it's set at BOF
        if the search was backward, and at EOF if the search was forward.

        NB: the current line is never evaluated. This is a feature, since
        we can so traverse occurrences with a

        line=f.findString("hello")
        while line == '':
            line.findString("hello")

        instead of playing with a readline every time to skip the current
        line.
        """
        internalcounter=1
        if count < 1:
            count = 1
        while 1:
            if backward == 0:
                line=self.readline()
            else:
                line=self.readbackline()

            if line == '':
                return ''
            if string.find(line,thestring) != -1 :
                if count == internalcounter:
                    return line
                else:
                    internalcounter = internalcounter + 1
                    # <<fold
    def findRegexp(self, theregexp, count=1, backward=0): # fold>>
        """
        find the count occurrence of the regexp in the file
        and return the line catched. The internal cursor is placed
        at the same line.
        backward is the searching flow.
        You need to pass a regexp string as theregexp.
        returns a tuple. The fist element is the matched line. The subsequent elements
        contains the matched groups, if any.
        If no match returns None
        """
        rx=re.compile(theregexp)
        internalcounter=1
        if count < 1:
            count = 1
        while 1:
            if backward == 0:
                line=self.readline()
            else:
                line=self.readbackline()

            if line == '':
                return None
            m=rx.search(line)
            if m != None :
                if count == internalcounter:
                    return (line,)+m.groups()
                else:
                    internalcounter = internalcounter + 1
    # <<fold
    def skipLines(self,key): # fold>>
        """
        skip a given number of lines. Key can be negative to skip
        backward. Return the last line read.
        Please note that skipLines(1) is equivalent to readline()
        skipLines(-1) is equivalent to readbackline() and skipLines(0)
        is equivalent to currentLine()
        """
        return self.__getitem__(self.__currentPos+key)
    # <<fold
    def occurrences(self,thestring,backward=0): # fold>>
        """
        count how many occurrences of str are found from the current
        position (current line excluded... see skipLines()) to the
        begin (or end) of file.
        returns a list of positions where each occurrence is found,
        in the same order found reading the file.
        Leaves unaltered the cursor position.
        """
        curpos=self.currentPos()
        list = []
        line = self.findString(thestring,1,backward)
        while line != '':
            list.append(self.currentPos())
            line = self.findString(thestring,1,backward)
        self.toPos(curpos)
        return list
        # <<fold
    def close(self): # fold>>
        self.__file.close()
    # <<fold



 

   