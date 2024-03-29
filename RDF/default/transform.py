import re

class Transform:
    """Example of query for create the input file:
    PREFIX cim: <http://iec.ch/TC57/2010/CIM-schema-cim15#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    DESCRIBE *
    WHERE {?GeographicalRegion rdf:type ?ID ."
    }"""
    
    def __init__(self): # fold>>
        self.lastTypeCim = ""
        self.file =""
        
    def transform(self, line, filein):
        matchAbout = re.search("rdf:about=", line)
        #extract the name of the file
        regexFile = ".*<rdf:Description rdf:about=\"file:///(.*)#"
        compiled_File = re.compile(regexFile)
        p = compiled_File.match(line)

        if p is not None:
            try:
                self.file = p.group(1)
            except:
                pass
        
        matchResource = re.search("rdf:resource=\"file:///"+self.file, line)
        matchDescription = re.search("/rdf:Description", line)
        matchType = re.search("<rdf:type rdf:resource=\"http://iec.ch/TC57/2010/CIM-schema-cim15#", line)
        matchDeleteTopo = re.search("<cim:Terminal.TopologicalNode", line) #delete Topological node
        matchDeleteIsland = re.search("<cim:TopologicalNode.TopologicalIsland", line) #delete Topological island
        if matchType:
            print "Delete line with type"
            #re.sub("<rdf:type rdf:resource=\"http://iec.ch/TC57/2010/CIM-schema-cim15#", "", type, count=0, flags=0)
            output= ""
            return output
        output = line
        if matchAbout:
            #print "About"
            output = self.transformAbout(line, filein)
            
        if matchResource:
            output = self.transformResource(line, filein)
            #print "Resource"
        if matchDescription:
            output = self.transformDescription(line, filein)
            #print "Description"
        if matchDeleteTopo:
            output = self.transformDeleteTopo(line, filein)
        return output
        
        if matchDeleteIsland:
            output = self.transformDeleteIsland(line, filein)
        return output   
        
    def transformAbout(self, line, filein):
        newLine = re.sub("rdf:about=\"file:///"+self.file+"#", "rdf:ID=\"", line, count=0, flags=0)
        print newLine
        key = filein.currentPos()
        type = filein.next()
        #print type
        #verify if it is the line with type
        matchType = re.search("<rdf:type rdf:resource=\"http://iec.ch/TC57/2010/CIM-schema-cim15#", type)
        typeCim = ""
        count = 1
        while typeCim == "":
            if matchType:
                print "Matched"
                typeCim = re.sub("<rdf:type rdf:resource=\"http://iec.ch/TC57/2010/CIM-schema-cim15#", "", type, count=0, flags=0)
                if count > 1:
                    #return at the correct line
                    filein.toPos(key)
                    #print key
                break
            else:
                count = count + 1
                type = filein.next()
                #print type
                #to do: verify that it is not "</rdf:Description...
                matchType = re.search("<rdf:type rdf:resource=\"http://iec.ch/TC57/2010/CIM-schema-cim15#", type)
            
            
        if count > 1:
            #print type
            matchType = re.search("<rdf:type rdf:resource=\"http://iec.ch/TC57/2010/CIM-schema-cim15#", type)
            if matchType:
                #print "Delete line with type"
                re.sub("<rdf:type rdf:resource=\"http://iec.ch/TC57/2010/CIM-schema-cim15#", "", type, count=0, flags=0)
        
        typeCimOriginal = typeCim 
        typeCim = typeCim[:-4]
        #typeCim = typeCim[4:]
        if(typeCim[3]==" "):
            typeCim = typeCim[4:]   
        elif(typeCim[2]==" "):
            typeCim = typeCim[3:]   
        if (typeCim == "ubstation"):
            print type
            print typeCimOriginal
            print typeCim
        typeCim = "cim:"+typeCim
        self.lastTypeCim = typeCim
            
        newLine = re.sub("rdf:Description", typeCim, newLine, count=0, flags=0)
        if newLine:
            #print "    "+newLine
            return newLine
        else:
            return line
    
    def transformResource(self,line, filein):
        newLine = re.sub("rdf:resource=\"file:///"+self.file, "rdf:resource=\"", line, count=0, flags=0)
        if newLine:
            #print "    "+newLine
            return newLine
        else:
            return line
        
    def transformDescription(self,line, filein):
        newLine =""
        if (re.search("/rdf:Description", line)):
            newLine = re.sub("/rdf:Description", "/"+self.lastTypeCim, line, count=0, flags=0)
            return newLine
        else:
            return line
        
    def transformDeleteTopo(self,line,filein):
        newLine =""
        if(re.search("<cim:Terminal.TopologicalNode", line)):
            return newLine
        else:
            return line
        
    def transformDeleteIsland(self,line,filein):
        newLine =""
        if(re.search("<cim:Terminal.TopologicalIsland", line)):
            return newLine
        else:
            return line