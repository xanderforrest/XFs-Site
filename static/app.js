function formatText(command, value) {
    document.execCommand(command)
}

function copyContent() {
    document.getElementById("content").value = document.getElementById("contentEditor").innerHTML;
    return True;
}

function testFunc() {
  document.getElementById("contentEditor").innerHTML += "<figure><img class='figure-img' src='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.fayettevilleflyer.com%2Fwp-content%2Fuploads%2F2015%2F09%2Fhozier.jpg&f=1&nofb=1' /><figcaption>Caption</figcaption></figure>"
}