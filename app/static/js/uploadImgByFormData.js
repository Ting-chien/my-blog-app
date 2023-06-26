const getFormData = (file) => {
  return new Promise((resolve, reject) => {
    const form = new FormData();
    form.append('uploadedFile', file);
    resolve(form)
  });
};

const uploadImg = async (pic) => {
    formData = await getFormData(pic)
    try {
      res = await fetch('/blog/upload-file-with-blob', { 
        method: 'POST', 
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        body: formData
      })
      displayImgByBufferArr(res.json()['img']);
    } catch(error) {
        // 錯誤處理 ...
        console.log(error)
    } finally {
        // 請求最後要做什麼（不管成功與否）...
        console.log(res)
    }
}
