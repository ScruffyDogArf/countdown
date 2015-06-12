
var app = {};


app.initialize = function () {

    $('.user-menu').on('click', function(e){
        e.preventDefault();
        $('.user-menu__dropdown', this).slideToggle('fast');
    });

    $('.add-icon').on('click', function(e){
        e.preventDefault();
        $('.modal__new-countdown').addClass('show');
    });

    $('.modal__new-countdown').on('click', function(e){
        e.preventDefault();
        if( e.target !== this )
            return;
        $('.modal__new-countdown').removeClass('show');
    });

    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1;
    var yyyy = today.getFullYear();

    $('.new-countdown-date').pickmeup({
        flat    : false,
        min     : dd+'-'+mm+'-'+yyyy
    });

    $('.submit input').on('click', function() {

        console.log('KAI :: submit click handler');
        app.createNewCountdown();
    });
};


app.createNewCountdown = function() {
    console.log('KAI :: creating new countdown');

    var title = "test";
    var description = "test description";
    var end_datetime = new Date();

    $.ajax({
        type: "POST",
        data: "title=" + title + "&description=" + description + "&end_datetime=" + end_datetime,
        url: "/api/countdowns/create" ,
        success: function(data) {
            if (data) {
                console.log('KAI ::', data);
            }
        },
        error: function(){
            console.log('KAI :: an error occured');
        }
    });
};

$( document ).ready(function() {
    app.initialize();
});