#reloading all files into datajs after editing
from os import listdir
from os.path import isfile, join
from Conv2HTML import readDataFile, writeDataFile


"""
Make reload method for entire file from text systems 
"""

def getMultiLineInput(msg):
    print(msg+"\n")
    print("Enter/Paste your content. Ctrl-Z to save it.\n")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    buf = ""
    for i in contents:
        buf += i+"\n"
    return buf

def getListOfFiles(readFromDirPath):
    listOfFiles = [join(readFromDirPath,f) for f in listdir(readFromDirPath) if isfile(join(readFromDirPath,f))] #total file path also
    return listOfFiles

def updateBlogFile(pathToFile,content):
    with open(pathToFile,'w', encoding="utf-8")  as f:
        f.write(content)
        f.close()
    return 

def Main():
    pathToDataJSFile = r"../js/data.js"
    blogPosts_location = r"../WriteBlogHere/"

    posts = readDataFile(pathToDataJSFile)
    id = int(input("Enter ID of post to edit: "))
    postToEdit = posts[id-1]
    updatedContent = getMultiLineInput(postToEdit)
    sureCheck = input("\nAre you sure you want to edit post (y/n): ")
    if sureCheck !="y":
        exit("Post Edit Aborted.")
    posts[id-1]=updatedContent
    #To get title
    titleStartIndex  = postToEdit.index("<b><u>")+len("<b><u>")
    titleEndIndex = postToEdit.index("</u></b>")
    title = postToEdit[titleStartIndex:titleEndIndex].strip()
    floc = join(blogPosts_location,f"{title}.txt")
    updateBlogFile(floc,updatedContent)
    writeDataFile(pathToDataJSFile,posts)    

    
if __name__ == "__main__":
    Main()

"""
NOTE: 
The actual saved text files exist only as a redundancy, i.e in case something goes horribly wrong when I updated some site mechanics/shift sites
I still retain the content. Them having added html doesn't matter, incase it makes my job easier in the future.
Ofc I could ignore all of them and just pick up data.js but its nice to have both layers.
"""
