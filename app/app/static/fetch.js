const form = document.querySelector('form');
const static_map_container = document.getElementsByName('static_map_container')[0];
const dynamic_map_container = document.getElementsByName('dynamic_map_container')[0];
const map_container = document.getElementsByName('map_container')[0];
const URL_s = "/static_plot";
const URL_d = "/dynamic_plot";

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const form_data = new FormData(form);
    let request_options = {
        method: "POST",
        headers: {
            // 'content-type': 'application/json'
        },
        body: form_data,
    }
    var URL = "";
    var type_plot = form_data.get("type_plot");
    if (type_plot == "Static"){
        URL = URL_s;
    }
    else if (type_plot == "Dynamic"){
        URL = URL_d;
    }
    
    fetch_plot(URL, request_options, type_plot);
})

function fetch_plot(URL, request_options, type_plot){
    fetch(URL, request_options)
    .then(response => response.json())
    .then((data) => {
        while (map_container.firstChild){
            map_container.firstChild.remove();
        }
        
        var d = document.createElement("div");

        if (type_plot == "Static"){
            d = document.createElement("div");
            d.innerHTML = data;
        }
        else {
            d.innerHTML = data["div"];
            var s = document.createElement("script");
            s.type = 'text/javascript';
            var scriptContent = document.createTextNode( data["script"]); 
            s.appendChild( scriptContent ); 
            d.appendChild(s);
        }
        map_container.appendChild(d);
    })
    .catch((err) => console.log(err))
}