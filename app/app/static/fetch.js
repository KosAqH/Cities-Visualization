const form = document.querySelector('form');
const static_map_container = document.getElementsByName('static_map_container')[0];
const dynamic_map_container = document.getElementsByName('dynamic_map_container')[0];

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

    const URL = "/static_plot";
    fetch_plot(URL, static_map_container);

    const URL2 = "/dynamic_plot";
    fetch_plot(URL2, dynamic_map_container);
})

function fetch_plot(URL, container){
    fetch(URL, request_options)
    .then(response => response.json())
    .then((data) => {
        container.appendChild(data);
    })
    .catch((err) => console.log(err))
}