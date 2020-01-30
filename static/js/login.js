window.addEventListener( "load", function () {
    function login() {
        const XHR = new XMLHttpRequest();

        // Bind the FormData object and the form element
        const FD = new FormData( form );

        // Define what happens on successful data submission
        XHR.addEventListener( "load", function(event) {
            var token = JSON.parse(event.target.responseText).token;
            if (token != null) {
                document.cookie = 'token=' + token + ';';
                document.location = '/';
            } else {
                document.location = '/login';
            }
        } );

        // Define what happens in case of error
        XHR.addEventListener( "error", function( event ) {
            alert( 'Oops! Something went wrong.' );
        } );

        // Set up our request
        XHR.open( "POST", "/login" );

        // The data sent is what the user provided in the form
        XHR.send( FD );
    }

    // Access the form element...
    let form = document.getElementById( "myForm" );

    // ...and take over its submit event.
    form.addEventListener( "submit", function ( event ) {
        event.preventDefault();

        login();
    } );
} );