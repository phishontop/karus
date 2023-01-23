
function sendLookup(input, modules, type) {
    const data = {
        kwargs: {[type]: input},
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

    let type = document.lookup["type"].value
    const modules = {
        name: ["minecraft", "github", "roblox", "steam"],
        fullname: ["companyhouse"],
        discord_id: ["discord"]
    };

    const modulesTicked = []

    for (var i = 0; i < modules[type].length; i++) {
        module = modules[type][i];
        if (document.lookup[module].checked) {
            modulesTicked.push(module)
        }
    }

    sendLookup(
        document.lookup["input"].value,
        modulesTicked,
        type
    );
}