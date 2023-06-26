// 將照片轉成 base64 string
function displayImgByBase64(blob) {
    const reader = new FileReader();
    // 這會在readAS後才執行
    reader.onload = function (e) {
        // Remove old image
        const oldImg = document.querySelector('#preview img');
        if (oldImg) {
            oldImg.remove();
        }
        // Add new image
        const img = document.createElement("img");
        img.className = "img-thumbnail w-50";
        img.style.height = "120px";
        img.setAttribute("src", e.target.result);
        document.querySelector('#preview').appendChild(img)
    };
    // to data url
    reader.readAsDataURL(blob);
}

// 讀取server端傳回來的array，將array轉回typed array，再將其變回 blob 並產生blob的url 
function displayImgByBufferArr(arr) {
    document.querySelector('#show-in-post').src = URL.createObjectURL(new Blob([new Uint8Array(arr)], {type: "image/png"}));
}
