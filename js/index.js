function getIndicesOf(searchStr, str, caseSensitive) {
    var searchStrLen = searchStr.length;
    if (searchStrLen == 0) {
        return [];
    }
    var startIndex = 0, index, indices = [];
    if (!caseSensitive) {
        str = str.toLowerCase();
        searchStr = searchStr.toLowerCase();
    }
    while ((index = str.indexOf(searchStr, startIndex)) > -1) {
        indices.push(index);
        startIndex = index + searchStrLen;
    }
    return indices;
}

//for now only removes the markers 
function FormatContent(unformattedContent){

    let str = unformattedContent;
    
    const startMarker = "<-$"
    const endMarker = "$->";

    var startIndices = getIndicesOf(startMarker,str,false);
    var endIndices = getIndicesOf(endMarker,str,false);

    let posts = [];
    let titles = []
    let dates = [];

    for(i of startIndices) {
        startIndex = i+startMarker.length;
        endIndex  = endIndices[startIndices.indexOf(i)];

        // console.log(startIndex);
        // console.log(endIndex);

        var post = str.substring(startIndex,endIndex)
        posts.push(post)
    }
    
    return posts;
}

function getDate(){
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = dd + '/' + mm + '/' + yyyy;
    return today
}

class BlogPost{
    title = "";
    content = "";
    dateTime = undefined;
}

function main(){    
    var formattedContent = gimmeContent();
    var toLoad = document.getElementsByClassName("blogPart")[0]
    for(x of formattedContent.reverse()){ //change this into a blog posts class and ID it according to title/date 
        toLoad.innerHTML += `<p class = "Loaded">${x}</p><br><br>`;
    }
}

main();
