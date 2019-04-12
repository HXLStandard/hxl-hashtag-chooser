// Progressive-enhancement script for HXL hashtag chooser

/**
 * Update the current display based on the hash.
 */
function updateHash() {
    var hash = location.hash;
    if (hash) {
        hash = hash.substr(1);
    } else {
        hash = "_top";
    }
    showSection(hash);
}

/**
 * Hide all sections except the one with the hash (id) provided
 */
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

// Fire updateHash whenever the user clicks on a link that changes the hash
window.addEventListener('hashchange', updateHash);

// Fire updateHash on start
window.onload = updateHash;
    
