function AddXMLRequestHooks(prehook, statehook) {
    var original_send = XMLHttpRequest.prototype.send
    XMLHttpRequest.prototype.send = function (body) {
        this.__intern_data.body = body
        if (prehook && prehook(this.__intern_data) === false) {
            // TODO: trigger error event
            return
        }
        var original_onreadystatechage = this.onreadystatechange
        this.onreadystatechange = () => {
            if (statehook)
                statehook(this, this.__intern_data)
            if (original_onreadystatechage)
                original_onreadystatechage()
        }
        return original_send.call(this, body)
    }
    var original_open = XMLHttpRequest.prototype.open
    XMLHttpRequest.prototype.open = function (method, url, async, user, password) {
        this.__intern_data = {
            method: method,
            url: url,
            async: async,
            user: user,
            password: password
        }
        return original_open.call(this, method, url, async, user, password)
    }
}