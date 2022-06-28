from os import listdir
from os.path import isfile, join, getctime
from datetime import datetime
import json as JSON

class post:
    def __init__(self,id,title,dateTime,content):
        self.id = id
        self.title = title
        self.dateTime = dateTime
        self.content = content

    def makeHtmlObj(self):
        # htmlStr = f'<div id="{self.id}" class="post"><b><u>{self.title}</u></b></div><br/><b>{self.dateTime}</b></br/>{self.content}</div>'
        htmlStr =f"""
<div id="{self.id}" class="post">
<b><u>{self.title}</u></b> Posted on {self.dateTime}
<br>
{self.content}
</div>
"""
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
    with open(filePath, 'r') as f:
        content = f.read()
        return content

def Main():
    readFromDirPath = r"../WriteBlogHere/"
    memoryPath = r"./memory.json"

    fileData = getJSON(memoryPath)

    lastCT = fileData["LastCTUnixStamp"] #what is this? OHH Created Time bruh
    postCount = fileData["PostCount"]

    format_ct = lambda ct: datetime.fromtimestamp(ct).strftime('%Y-%m-%d %H:%M')

    listOfFiles = [f for f in listdir(readFromDirPath) if isfile(join(readFromDirPath,f))]
    ctimes = [getctime(join(readFromDirPath,f)) for f in listOfFiles]
    formattedCT = [format_ct(t) for t in ctimes]

    #Im going to be honest here, I wrote this a while ago but I forgot what it does but I know it's important 
    couples = [(x,formattedCT[i]) for i,x in enumerate(ctimes)]

    #format of the dict -> {'Blog Title.txt': (CT_Float, formattedCT_String),..}
    postsDict = dict(zip(listOfFiles,couples)) #Dictionary Filled With All the File Data from the ./WriteBlogHere directory

    for p in postsDict:
        
        ct = postsDict[p][0] #Taking the created time of the post in the posts dict

        if ct>lastCT: #If the post is new, it's value will be greater than the last created time. We loaded the last created time from the memory.json file
            print("New Post Found!")
            print(f"Processing {p}...")

            fp = join(readFromDirPath,p) #filePath 
            title = p[:-4]
            date = postsDict[p][1]
            content = readFileContent(fp)
            id = postCount+1 #we got the last known post count again from memory.json

            newPost = post(id,title,date,content) #We create a new post object 
            
            #Now it's the saving part, the things to save are as follows:
            #We have Firstly Update memory.json with both a new timeStamp and post count
            #Secondly (the more tricky one), we navigate to ./js/data.js (wrt to main directory) and then save the html part inside the list 

            #Updating JSON
            lastCT=ct
            fileData["LastCTUnixStamp"] = lastCT
            fileData["PostCount"] = id
            saveJson(memoryPath,fileData)
            print("Memory Updated.")

            #Updating data.js

            dataJSPath = r"../js/data.js"

            with open(dataJSPath,'r') as dataF:
                data = dataF.read()
                s = data.index('/*startIndex*/')
                e = data.index('/*endIndex*/')
                myList = eval(data[s+len("/*startIndex*/"):e]) #LMAO LETS GOOOO
            
            myList.append(newPost.makeHtmlObj())

            with open(dataJSPath,'w') as dataF:
                #How tf is this even allowed man
                fileContent = f"""
var blogContent =  /*startIndex*/{myList}/*endIndex*/"""+'\n'+"function gimmeContent(){return blogContent}"
                dataF.write(fileContent)
            print("data.js Updated.")
Main()


"""
Load JSON Values -- done
Look at dict and check for new uploads -- done
if new upload(s) then take each new upload, take the title, create time and content and put it in the template form --done
take that post from the template you made (make a class its easier to make an object then) --done
then shove that object in data.js 
figure out what to do from there later
"""