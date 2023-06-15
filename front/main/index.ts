import axios from "axios";
import { Chart } from "chart.js/auto";

for (let node of document.querySelectorAll(".graph")) {
    const canvas = node as HTMLCanvasElement
    const url = canvas.dataset.src
    if (url === undefined) {
        continue
    }
    axios.get(url).then((response) => {
        console.log(response)
        new Chart(
            canvas,
            response.data
        );
    })
}