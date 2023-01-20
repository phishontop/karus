
function sendLookup(name, modules) {
    const data = {
        name: name,
        modules: modules
    };

    fetch("/api/lookup", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(response => document.getElementById("json").innerHTML = JSON.stringify(response, undefined, 2))
}


function getResults() {
    const modules = ["minecraft", "github", "roblox", "steam"];
    const modulesTicked = []

    for (var i = 0; i < modules.length; i++) {
        module = modules[i];
        if (document.lookup[module].checked) {
            modulesTicked.push(module)
        }
    }

    sendLookup(document.lookup["name"].value, modulesTicked);
}
