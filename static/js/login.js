function login() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    var request = new XMLHttpRequest();
    request.open("POST", '/login', true);
    request.onload = function() {
        var token = JSON.parse(request.responseText).token;
        if (token != null) {
            document.cookie = 'token=' + token + ';';
            document.location = '/';
        } else {
            alert('No can do');
        }
    }
    request.send(JSON.stringify({
        email: email,
        password: password
    }));
}