// Progressive-enhancement script for HXL hashtag chooser

function getHash() {
    var hash = location.hash;
    if (hash) {
        hash = hash.substr(1);
    } else {
        hash = "_top";
    }
    return hash;
}

function showSection(hash) {
    var nodes = document.getElementsByTagName("section");
    for (var i = 0; i < nodes.length; i++) {
        var node = nodes.item(i);
        if (node.id == hash) {
            node.style.display = "block";
        } else {
            node.style.display = "none";
        }
    }
}

function updateHash() {
    var hash = getHash();
    console.log("Hash change!", hash);
    showSection(hash);
}

window.addEventListener('hashchange', updateHash);
    
window.onload = updateHash;
    
