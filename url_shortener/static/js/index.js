function copyToClipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();
}

function checkvalue() {
    var mystring = $('#urlLong').val();
    if(!mystring.match(/\S/)) {
        return false;
    } else {
        return true;
    }
}
