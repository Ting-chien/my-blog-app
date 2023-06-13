
var isExpand = false

function getMessages() {

    const notification = document.querySelector(".notification")
    console.log(isExpand)
    if (isExpand) {
        list = document.querySelector("ul.message-list")
        if (list) {
            list.remove()
        }
        isExpand = false
    } else {
        fetch('http://127.0.0.1:3000/blog/get-messages', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "id": 78912 })
        })
        .then(response => response.json())
        .then(response => {
            data = response["data"]
            if (data) {
                const newList = document.createElement("ul")
                newList.className = "dropdown-menu show message-list"
                for (const d of data) {
                    item = document.createElement("li")
                    link = document.createElement("a")
                    link.className = "dropdown-item"
                    link.innerHTML = d.content
                    item.append(link)
                    newList.appendChild(item)
                }
                notification.append(newList)
                isExpand = true
            }

        })
    }
}