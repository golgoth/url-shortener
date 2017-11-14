function copyToClipboard() {
  var copyText = document.getElementById("shortUrl");
  copyText.select();
  document.execCommand("Copy");
}
