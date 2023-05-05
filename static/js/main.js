
const dropbox = document.getElementById("upload-zone");
const preview = document.getElementById("preview");

// function handleFileSelect(e) {
//     debugger;
//     e.stopPropagation();
//     e.preventDefault();
//     const fileUploader = document.getElementById("fileUploader");
//     fileUploader.click();
//     dropbox.classList.remove("upload_zone_enter");
// }

const click = e => handleFileSelect(e);

// prevent the default method working
function dragenter(e) {
    // add the styling to div
    dropbox.classList.add("upload-zone--enter");
    e.stopPropagation();
    e.preventDefault();
}

const dragleave = () => dropbox.classList.remove("upload-zone--enter");

// prevent the default method working
function dragover(e) {
    e.stopPropagation();
    e.preventDefault();
}

function handleFiles(files) {
    dropbox.classList.remove("upload-zone--enter");
    for (var i = 0; i < files.length; i++) {
        const file = files[i];
        const imageType = /image.*/;

        if (!file.type.match(imageType)) {
            continue;
        }

        const img = document.createElement("img");
        img.classList.add("obj");
        img.file = file;
        preview.appendChild(img);

        const reader = new FileReader();
        reader.onload = (e => img.src = e.target.result);
        reader.readAsDataURL(file);
    }
}

function drop(e) {
    e.stopPropagation();
    e.preventDefault();

    const dt = e.dataTransfer;
    const files = dt.files;
    document.getElementById("fileUploader").files = files
    handleFiles(files);
    dropbox.classList.remove("upload-zone--enter");
    dropbox.style.display = "none";
}

dropbox.addEventListener("click", click, false);
dropbox.addEventListener("dragenter", dragenter, false);
dropbox.addEventListener("dragleave", dragleave, false);
dropbox.addEventListener("dragover", dragover, false);
dropbox.addEventListener("drop", drop, false);
function showLoading() {
    const submitButton = document.getElementById("submit");
    submitButton.disabled = true;
    
    // Create the loading element
    const loading = document.createElement('div');
    loading.classList.add('loading');
    document.body.appendChild(loading);
  }
document.getElementById("upload_form").addEventListener("submit", function (e){
    e.preventDefault();
    showLoading();
    const thought = document.getElementById("thought").value;
    const fileInput = document.getElementById("fileUploader");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("thought", thought);
    formData.append("file", file);

    fetch("/", {
        method: "POST",
        body: formData
      }).then(function(response) {
        return response.text(); // Get response body as text
      }).then(function(filename) {
        const submitButton = document.getElementById("submit");
        submitButton.disabled = false;
        const poster = document.querySelector(".poster__img");
        poster.setAttribute("src",  filename);
      });
});