const canvas = document.getElementById('sketch-board');
const context = canvas.getContext('2d');

const width = 500;
const height = 500;

canvas.width = width;
canvas.height = height;

let isMouseDown = false;
let previousPoint;

context.fillStyle = "#fff";
context.strokeStyle = "black";
context.lineJoin = "round";
context.lineWidth = 5;
context.fillRect(0, 0, width, height);

let imgPreview = document.querySelector("#img-preview");
let imgResults = document.querySelector("#results");

canvas.addEventListener('mousedown', (event) => {
    isMouseDown = true;
});

canvas.addEventListener('mousemove', (event) => {
    if (isMouseDown) {
        console.log("Drawing...");
        let boundary = canvas.getBoundingClientRect();
        let mouseX = event.clientX - boundary.left;
        let mouseY = event.clientY - boundary.top;

        // context.fillStyle = "white";
        // context.fillRect(mouseX, mouseY, 1, 1);

        let currentPoint = {
            x: mouseX,
            y: mouseY
        };

        if (!previousPoint) {
            previousPoint = currentPoint;
        }

        context.beginPath();
        context.moveTo(previousPoint.x, previousPoint.y);
        context.lineTo(currentPoint.x, currentPoint.y);
        context.closePath();
        context.stroke();

        previousPoint = currentPoint;
    }
});

// canvas.addEventListener('mouseleave', (event) => {
//     isMouseDown = false;
//     previousPoint = null;
// });

canvas.addEventListener('mouseup', (event) => {
    isMouseDown = false;
    previousPoint = null;
});

document.querySelector('#btn-clear').addEventListener('click', (event) => {
    context.clearRect(0, 0, width, height);
    context.fillRect(0, 0, width, height);

    imgResults.innerHTML = '';
    imgPreview.src = '';
});

document.querySelector('#btn-submit').addEventListener('click', (event) => {
    imgPreview.src = canvas.toDataURL();
    upload();
});

function upload() {
    let imageDataBase64 = document.querySelector("#img-preview").src;
    if (!imageDataBase64) {
        console.log("No preview image");
        return;
    }

    imageDataBase64 = imageDataBase64.split(",")[1];

    fetch
        ('/api/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                img: imageDataBase64
            })
        })
        .then(response => response.json())
        .then(response => {
            imgResults.innerHTML = '';
            for (let src of response) {
                let img = `<img alt="" src="${src}"/>`;
                imgResults.innerHTML += img;
            }
        })
        .catch(error => console.error(error));
}