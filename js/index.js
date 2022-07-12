function main(){    
    var formattedContent = gimmeContent();
    var toLoad = document.getElementsByClassName("blogPart")[0]
    for(x of formattedContent.reverse()){ //reversed so that newest posts pop up first
        toLoad.innerHTML += `<p class = "Loaded">${x}</p><br><br>`;
    }
}

main();