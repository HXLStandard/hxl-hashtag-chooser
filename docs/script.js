////////////////////////////////////////////////////////////////////////
// Progressive-enhancement script for HXL hashtag chooser
//
// The chooser will work without this code; it simply hides inactive
// sections in modern browsers so that users can't accidentally scroll
// to them.
////////////////////////////////////////////////////////////////////////

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
 * Add a copy to clipboard option, if supported.
 */
function addCopyButtons() {
    var nodes = document.getElementsByClassName("final-tagspec");
    for (var i = 0; i < nodes.length; i++) {
        var tagspecNode = nodes.item(i);
        var buttonNode = document.createElement("button");
        buttonNode.className = "copy-button";
        buttonNode.innerHTML = "&#x1f4cb;";
        buttonNode.title = "Copy to clipboard";
        buttonNode.onclick = (ev) => {
            // to copy, temporarily create an <input> element
            var buttonNode = ev.target;
            var tagspecNode = buttonNode.previousSibling;
            var inputNode = document.createElement("input");
            tagspecNode.parentNode.insertBefore(inputNode, tagspecNode.nextSibling);
            inputNode.value = tagspecNode.innerHTML;
            inputNode.focus();
            inputNode.select();
            document.execCommand("copy");
            tagspecNode.parentNode.removeChild(inputNode);
        };
        tagspecNode.parentNode.insertBefore(buttonNode, tagspecNode.nextSibling);
    }
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


window.onload = () => {

    // do we support hashchange events?
    // if so, hide all but the active section
    if ("onhashchange" in window) {
        updateHash();
        window.addEventListener('hashchange', updateHash);
    }

    // do we support execCommand?
    // if so, add a copy-to-clipboard button for every result
    if ("execCommand" in document) {
        addCopyButtons();
    }
};
