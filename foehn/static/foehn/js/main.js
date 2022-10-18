"use strict";

function load_json(url, callback) {
    const httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
                let data = JSON.parse(httpRequest.response)
                callback(data)
            }
        }
    }
    httpRequest.open("GET", url)
    httpRequest.send()
}

function main() {
    for (let canvas of document.querySelectorAll(".graph")) {
        load_json(canvas.dataset.src, (config) => {
            new Chart(
                canvas,
                config
            );
        });
    }
}


document.addEventListener("DOMContentLoaded", main)