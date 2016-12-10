function snorlax(newurl) {
    this.myurl = newurl;

    this.find = function(get, by, paramString, callback) {
        console.log(this.myurl + '/' + get +'/' + by + paramString);
        $.ajax({
            type: 'GET',
            url: this.myurl + '/' + get +'/' + by + paramString,
            contentType: 'application/json',
            success: callback,
            error: function(req, status, ex) {},
            timeout:60000
        });
    };
}