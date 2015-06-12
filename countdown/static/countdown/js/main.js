
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

};

$( document ).ready(function() {
    app.initialize();
});