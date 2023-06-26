// 將照片轉成 base64 string
function displayImgByBase64(blob) {
    const reader = new FileReader();
    // 這會在readAS後才執行
    reader.onload = function (e) {
        // console.log('file:', e.target.result); // base64
        document.querySelector('#preview').src = e.target.result;
    };
    // to data url
    reader.readAsDataURL(blob);
}

// 讀取server端傳回來的array，將array轉回typed array，再將其變回 blob 並產生blob的url 
function displayImgByBufferArr(arr) {
    document.querySelector('#preview').src = URL.createObjectURL(new Blob([new Uint8Array(arr)], {type: "image/png"}));
}
