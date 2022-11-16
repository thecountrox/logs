from os import listdir
from os.path import isfile, join, getctime
from datetime import datetime
import json as JSON
import markdown

class post:
    def __init__(self,id,title,dateTime,content):
        self.id = id
        self.title = title
        self.dateTime = dateTime
        self.content = content

    def makeHtmlObj(self):
        htmlStr =f"""<div id="{self.id}" class="post"><b><u>{self.title}</u></b> Posted on {self.dateTime}<br>{self.content}</div>"""
        return htmlStr

def getJSON(filePath):
    with open(filePath, 'r') as f:
        jsonValue = f.read()
        return JSON.loads(jsonValue)

def saveJson(filePath,changedDict):
    with open(filePath, 'w') as f:
        JSON.dump(changedDict,f)
    return 

def readFileContent(filePath):
    with open(filePath, 'r',encoding='utf-8') as f:
        content = f.read()
        return content

def readDataFile(dataJSPath):
    with open(dataJSPath,'r',encoding='utf-8') as dataF:
        data = dataF.read()
        s = data.index('/*startIndex*/')
        e = data.index('/*endIndex*/')
        myList = eval(data[s+len("/*startIndex*/"):e]) 
    return myList 

def writeDataFile(dataJSPath,myList):
    with open(dataJSPath,'w',encoding="utf-8") as dataF:
        fileContent = f"""var blogContent =  /*startIndex*/{myList}/*endIndex*/"""+'\n'+"function gimmeContent(){return blogContent}"
        dataF.write(fileContent)
    print("data.js Updated.")

def sortDictByDateTime(someDict):
    return dict(sorted(someDict.items(), key=lambda item: item[1][0]))

def MakeNewPost(postName,postDate,memoryObj,blogDirPath): #postName and post title are the same, opening file name is what we wanna achieve here 
    # fileData = getJSON(memPath) file data is nothing by memoryJSON
    #lastCT = fileData["LastCTUnixStamp"] #what is thi\s? OHH Created Time bruh
    #postDate is human readable date format

    pathOfNewPost = join(blogDirPath,postName) #path of file to append 

    if(pathOfNewPost[-1:-4:-1]=="txt"):
        title = postName[:-4]
    elif (pathOfNewPost[-1:-3:-1]=="dm"): #hack for .md files
        title = postName[:-3]
    else:
        exit("Invalid File Type!...only md / txt files are accepted.")

    print(f"Title is {title}")

    content = readFileContent(pathOfNewPost) #For New Version the entered content will be in markdown, we convert it to html with the parser
    parsedContent = markdown.markdown(content,extensions=['pymdownx.tilde'])
    
    postCount = memoryObj["PostCount"]
    postCount = postCount+1 #we got the last known post count again from memory.json
    id = postCount

    newPost = post(id,title,postDate,parsedContent) #We create a new post object 

    return newPost
            
def AppendNewPost(newPostObj, memoryObject, createTimeUNIX, djsPath, memJSONPath):

    postID = newPostObj.id

    #Updating JSON
    memoryObject["LastCTUnixStamp"] = createTimeUNIX
    memoryObject["PostCount"] = postID
    saveJson(memJSONPath,memoryObject)
    print("Memory Updated.")

    #Updating data.js
    myList = readDataFile(djsPath)
    myList.append(newPostObj.makeHtmlObj()) #I am stupid.
    writeDataFile(djsPath,myList)
    

def Main():
    readFromDirPath = r"../WriteBlogHere/"
    memoryPath = r"./memory.json"
    dataJSPath = r"../js/data.js"

    fileData = getJSON(memoryPath)

    lastCT = fileData["LastCTUnixStamp"] #what is this? OHH Created Time bruh

    format_ct = lambda ct: datetime.fromtimestamp(ct).strftime('%Y-%m-%d %H:%M')

    listOfFiles = [f for f in listdir(readFromDirPath) if isfile(join(readFromDirPath,f))]
    ctimes = [getctime(join(readFromDirPath,f)) for f in listOfFiles]
    formattedCT = [format_ct(t) for t in ctimes]

    #Im going to be honest here, I wrote this a while ago but I forgot what it does but I know it's important  (it makes a (title,timestamp) couple)
    couples = [(x,formattedCT[i]) for i,x in enumerate(ctimes)]

    #format of the dict -> {'Blog Title.txt': (CT_Float, formattedCT_String),..}
    postsDict = dict(zip(listOfFiles,couples)) #Dictionary Filled With All the File Data from the ./WriteBlogHere directory
    postsDict = sortDictByDateTime(postsDict)

    for p in postsDict:        

        ct = postsDict[p][0] #Taking the created time (UNIX) of the post in the posts dict
        humanReadableDate = postsDict[p][1] 

        if ct>lastCT: #If the post is new, it's value will be greater than the last created time. We loaded the last created time from the memory.json file
            print("New Post Found!")
            print(f"Processing {p}...")
            
            np = MakeNewPost(p, humanReadableDate, fileData, readFromDirPath)
            AppendNewPost(np, fileData, ct, dataJSPath, memoryPath)

if __name__ == "__main__":
    Main()