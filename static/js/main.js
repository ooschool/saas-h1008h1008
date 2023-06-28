
const dropbox = document.getElementById("upload-zone");
const preview = document.getElementById("preview");
<<<<<<< Updated upstream

// function handleFileSelect(e) {
//     debugger;
//     e.stopPropagation();
//     e.preventDefault();
//     const fileUploader = document.getElementById("fileUploader");
//     fileUploader.click();
//     dropbox.classList.remove("upload_zone_enter");
// }
=======
var thoughtInput = document.getElementById("rand");
thoughtInput.style.display = "none"
var elements = document.querySelectorAll('#randtext');
for (var i = 0; i < elements.length; i++) {
  elements[i].style.display = 'none';
}
document.getElementById("load").style.display = "none"
document.getElementById("over").style.display = "none"
document.getElementById("productdd").style.display = "none"
var globalFlag = 'poster';
var randButton = document.getElementById("rand");

randButton.addEventListener("click", function() {
  // 執行 submit 按鈕的相應操作
  showLoading();
  const formData1 = new FormData();
  formData1.append("flag", 'rand');
  fetch("/", {
    method: "POST",
    body: formData1
  }).then(function(response) {
    return response.json(); // Parse response body as JSON
  }).then(function(data) {
    document.getElementById("load").style.display = "none"
    document.getElementById("over").style.display = "none"
    const submitButton = document.getElementById("submit");
    submitButton.disabled = false;
    var texts = data.filename.split(/\d+\./).filter(Boolean).map(function(text) {
      return text.trim();
    });
    var elements = document.querySelectorAll('#randtext');
    for (var i = 0; i < elements.length; i++) {
      if (i < texts.length) {
        elements[i].textContent = texts[i];
      }
    } 
  });
});
// Get the "Poster Maker" choice element
const posterMakerChoice = document.getElementById('posterd');

// Add a click event listener to the "Poster Maker" choice
posterMakerChoice.addEventListener('click', function() {
  document.getElementById("productdd").style.display = "none"
  // Set the global flag to 1
  globalFlag = 'poster';
  const exampleElement = document.getElementById("example");
  var thoughtInput = document.getElementById("rand");
  thoughtInput.style.display = "none"
  var elements = document.querySelectorAll('#randtext');
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.display = 'none';
  }
  dropbox.style.display = "block";
  exampleElement.innerText = "Poster Maker!";
  var thoughtInput = document.getElementById("thought");
  thoughtInput.value = "";
  thoughtInput.placeholder = "2.請輸入期望背景長相";
  const poster = document.querySelector(".poster__img");
  poster.setAttribute("src",  '/static/images/20230330114934PM.jpg');
  const randtextDiv = document.getElementById("instr");
  randtextDiv.innerHTML = 'Your Poster';
},false);
const Choice = document.getElementById('productd');

// Add a click event listener to the "Poster Maker" choice
Choice.addEventListener('click', function() {
  document.getElementById("productdd").style.display = "block"
  // Set the global flag to 1
  globalFlag = 'product';
  const exampleElement = document.getElementById("example");
  var thoughtInput = document.getElementById("thought");
  thoughtInput.value = "";
  thoughtInput.placeholder = "1.請輸入期望商品長相";
  var thoughtInput = document.getElementById("rand");
  var elements = document.querySelectorAll('#randtext');
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.display = 'block';
  }
  thoughtInput.style.display = "block"
  dropbox.style.display = "none";
  preview.innerHTML = ""; // 清空內容
  preview.style.display = "none";
  exampleElement.innerText = "Product Designer!";
  const poster = document.querySelector(".poster__img");
  poster.setAttribute("src",  '/static/images/20230330114934PM.jpg');
  const randtextDiv = document.getElementById("instr");
  randtextDiv.innerHTML = 'Your Poster';
},false);
>>>>>>> Stashed changes

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
var optionDivs = document.getElementsByClassName('option');

// 为每个 div 元素添加点击事件监听器
for (var i = 0; i < optionDivs.length; i++) {
  optionDivs[i].addEventListener('click', function() {
    showLoading();
    const thought =  this.textContent;
    console.log(thought);
    const formData = new FormData();
    formData.append("thought", thought);
    formData.append("flag", 'product');
    fetch("/", {
      method: "POST",
      body: formData
    }).then(function(response) {
      return response.json(); // Parse response body as JSON
    }).then(function(data) {
      document.getElementById("load").style.display = "none"
      document.getElementById("over").style.display = "none"
      const submitButton = document.getElementById("submit");
      submitButton.disabled = false;
      const poster = document.querySelector(".poster__img");
      poster.setAttribute("src",  data.filename);
      const randtextDiv = document.getElementById("instr");
      randtextDiv.innerHTML = data.title;
    });
  });
}
document.getElementById("upload_form").addEventListener("submit", function (e){
    e.preventDefault();
    showLoading();
    const thought = document.getElementById("thought").value;
    const fileInput = document.getElementById("fileUploader");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("thought", thought);
<<<<<<< Updated upstream
    formData.append("file", file);

=======
    if (globalFlag === 'poster') {
      // Code to be executed if globalFlag is equal to 0
      formData.append("file", file);
      // Additional code here...
    }
    formData.append("flag", globalFlag);
>>>>>>> Stashed changes
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