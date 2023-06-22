
const dropbox = document.getElementById("upload-zone");
const preview = document.getElementById("preview");
var thoughtInput = document.getElementById("rand");
thoughtInput.style.display = "none"
document.getElementById("randtext").style.display = "none"
document.getElementById("load").style.display = "none"
document.getElementById("over").style.display = "none"
var globalFlag = 0;
var randButton = document.getElementById("rand");

randButton.addEventListener("click", function() {
  // 執行 submit 按鈕的相應操作
  showLoading();
  const formData1 = new FormData();
  formData1.append("flag", 2);
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
    var randtextDiv = document.getElementById("randtext")
  // Replace the content of the <div> with the replacement text
    randtextDiv.innerHTML = data.filename;
  });
});
// Get the "Poster Maker" choice element
const posterMakerChoice = document.getElementById('posterd');

// Add a click event listener to the "Poster Maker" choice
posterMakerChoice.addEventListener('click', function() {
  // Set the global flag to 1
  globalFlag = 0;
  const exampleElement = document.getElementById("example");
  var thoughtInput = document.getElementById("rand");
  thoughtInput.style.display = "none"
  document.getElementById("randtext").style.display = "none"
  dropbox.style.display = "block";
  exampleElement.innerText = "Poster Maker!";
  var thoughtInput = document.getElementById("thought");
  thoughtInput.value = "";
  thoughtInput.placeholder = "2.請輸入期望背景長相";
},false);
const Choice = document.getElementById('productd');

// Add a click event listener to the "Poster Maker" choice
Choice.addEventListener('click', function() {
  // Set the global flag to 1
  globalFlag = 1;
  const exampleElement = document.getElementById("example");
  var thoughtInput = document.getElementById("thought");
  thoughtInput.value = "";
  thoughtInput.placeholder = "1.請輸入期望商品長相";
  var thoughtInput = document.getElementById("rand");
  document.getElementById("randtext").style.display = "block"
  thoughtInput.style.display = "block"
  dropbox.style.display = "none";
  preview.innerHTML = ""; // 清空內容
  preview.style.display = "none";
  exampleElement.innerText = "Product Designer!";
},false);

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
    preview.style.display = "block";
}

dropbox.addEventListener("click", click, false);
dropbox.addEventListener("dragenter", dragenter, false);
dropbox.addEventListener("dragleave", dragleave, false);
dropbox.addEventListener("dragover", dragover, false);
dropbox.addEventListener("drop", drop, false);
function showLoading() {
    const submitButton = document.getElementById("submit");
    submitButton.disabled = true;
    document.getElementById("load").style.display = "block"
    document.getElementById("over").style.display = "block"
    // Create the loading element
  }
document.getElementById("upload_form").addEventListener("submit", function (e){
    e.preventDefault();
    showLoading();
    const thought = document.getElementById("thought").value;
    const fileInput = document.getElementById("fileUploader");
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("thought", thought);
    if (globalFlag === 0) {
      // Code to be executed if globalFlag is equal to 0
      formData.append("file", file);
      // Additional code here...
    }
    formData.append("flag", globalFlag);
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
var choices = document.getElementsByClassName('choice');

// 監聽鼠標移動事件
document.addEventListener('mousemove', function(event) {
  // 獲取當前鼠標的座標
  var mouseX = event.clientX;
  var mouseY = event.clientY;

  // 迭代所有 "choice" 元素
  for (var i = 0; i < choices.length; i++) {
    var choice = choices[i];
    
    // 獲取 "choice" 元素的位置和尺寸
    var rect = choice.getBoundingClientRect();
    var choiceX = rect.left;
    var choiceY = rect.top;
    var choiceWidth = rect.width;
    var choiceHeight = rect.height;

    // 檢查鼠標是否在 "choice" 元素的範圍內
    if (mouseX >= choiceX && mouseX <= choiceX + choiceWidth &&
        mouseY >= choiceY && mouseY <= choiceY + choiceHeight) {
      // 在 "choice" 元素範圍內，將顏色變深一點
      choice.style.filter = 'brightness(85%)';
      choice.style.cursor = 'pointer';
    } else {
      // 不在 "choice" 元素範圍內，恢復原始顏色
      choice.style.filter = 'none';
    }
  }
});