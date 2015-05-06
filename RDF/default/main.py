from fileReader import FileReader
from transform import Transform

fileNameInput = "/home/bionda/Documents/eclipse/workspace/TransformRDF/input/prova.xml"
#fileNameInput = "C:\\data\\others\\lambrate_solo_CESI.xml"
#fileNameOutput = "C:\\data\\others\\lambrate_solo_CESI_cim.xml"
fileNameOutput = "/home/bionda/Documents/eclipse/workspace/TransformRDF/output/prova_cim.xml"
#fileNameInput = "C:\\data\\others\\novate_generators.xml"
#fileNameOutput = "C:\\data\\others\\novate_generators_cim.xml"
tr = Transform()
read = "r"
write = "w"
fi = FileReader(fileNameInput, read)
#fo = FileReader(fileNameOutput, write)
fo = open(fileNameOutput, write)
#fw = open("C:\data\others\sub_created.xml", "w")


#lineIn = fi.readline()
print "Started transform"
fo.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
fo.write("\n")
while fi.next():
    lineIn = tr.transform(fi.currentLine(), fi)
    #print lineIn
    fo.write(lineIn)

fo.close()
fi.close()
print "Finished transform"