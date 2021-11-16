import os.path

filename = "/tmp/stored_message.data"

def readFilePrintMessages():
    out = set([])
    if not os.path.exists(filename):
        return out
    fw = open(filename, "r")
    for line in fw:
        #print("data in file is:",line, line [:-1])
        line=line[:-1]
        out.add(line)
    return out

def  writeMessageToFile(messages):
    out = set([])
    #we want to open in append mode, so we can add to the file
    fw = open(filename, "a")
    for message in messages:
        print("Writing message:", message.id)
        if message.id in out:
            continue
        print("Wrote message:" , message.id)
        fw.write(str(message.id)+"\n")
        out.add(message.id)


readFilePrintMessages()