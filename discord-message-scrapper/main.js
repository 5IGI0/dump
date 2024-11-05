(function () {
    var processed_messages = new Set();
    var export_data = ""

    AddXMLRequestHooks(null,function (xhr, infos) {
        if (xhr.readyState == 4 && infos.url.includes("/messages")) {
            data = JSON.parse(xhr.responseText)
            for (var i = 0; i < data.length; i++) {
                if (processed_messages.has(data[i].id) == false) {
                    export_data += JSON.stringify(data[i]) + "\r\n"
                    if (export_data.length > 1_000_000) {
                        let date = new Date();
                        saveBlobAsText(export_data, "discrape-"+date.toISOString()+".json")
                        export_data = ""
                    }
                }
            }
        }
    })

    setInterval(() => {
        document.querySelector("body>div>div>div>div>div>div>div>div>div>div>div>div>main>div>div").scrollTop=0
        //document.evaluate("body>div>div>div>div>div>div>div>div>div>div>div>div>main>div>divv", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
    }, 5000)
})()

