// 將 blob 轉乘 array buffer
function blob2buffer(blob) {
    return new Promise((resolve, reject) => {
        var arrayBuffer;
        var fileReader = new FileReader();
        fileReader.onload = function (event) {
            arrayBuffer = event.target.result;
            resolve(arrayBuffer);
        };

        fileReader.readAsArrayBuffer(blob);
        return arrayBuffer;
    });
}

// 因為 buffer 不能直接被操作，因此須先將圖片轉成 array buffer 再轉乘 string 再丟給後端
async function uploadImg(pic) {
    arrayBuffer = await blob2buffer(pic);

    fetch("/blog/upload-file-with-buffer", {
        method: 'POST',
        headers: {
            'content-type': 'application/json' // flask need to set header of json
        },
        body: JSON.stringify({
            item_id: 1,
            format: 'png',
            img: Array.from(new Uint8Array(arrayBuffer)),
        }),
    }).then((res)=> {
        return res.json()
    }).then((json) => {
        displayImgByBufferArr(json['img']);
    })
}