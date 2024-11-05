function saveBlobAsText(text, filename) {
    let blob = new Blob([text], {type: 'application/json'});
    let url = URL.createObjectURL(blob);
    let link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}