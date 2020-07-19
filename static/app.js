function formatText(command, value) {
    document.execCommand(command)
}

function copyContent() {
    document.getElementById("content").value = document.getElementById("contentEditor").innerHTML;
    return True;
}