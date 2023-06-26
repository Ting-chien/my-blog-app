const addPost = async () => {

    // Retrieve form value
    const form = document.querySelector("form#new-post")
    const title = form.querySelector("#title").value
    const content = form.querySelector("#content").value
    const img = form.querySelector("#file-upload-selector").files[0]
    console.log(img)
    // Transform blob to array buffer
    arrayBuffer = await blob2buffer(img);

    // Send post request
    await fetch("/blog/add-post", {
        method: 'POST',
        headers: {
            'content-type': 'application/json' // flask need to set header of json
        },
        body: JSON.stringify({
            title: title,
            content: content,
            img: Array.from(new Uint8Array(arrayBuffer)),
        }),
    })

    window.location.href = "/blog"
}