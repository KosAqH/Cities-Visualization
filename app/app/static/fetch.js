const form = document.querySelector('form');
const static = document.getElementsByName('static_map_container')[0];

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const form_data = new FormData(form);
    // const form_data = new FormData(e.target);
    let request_options = {
        method: "POST",
        headers: {
            // 'content-type': 'application/json'
        },
        body: form_data,
    }

    console.log(request_options);

    const URL = "/static_plot"

    fetch(URL, request_options)
    .then(response => response.json())
    .then((data) => {
        static.innerHTML = data;
    })
    .catch((err) => console.log(err))
})

