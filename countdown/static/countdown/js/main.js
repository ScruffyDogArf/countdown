;( function( $, window, document, undefined )
{
    'use strict';

    var $list       = $( '.grid' ),
        $items      = $list.find( '.countdown' ),
        setHeights  = function()
        {
            $items.css( 'height', 'auto' );

            var perRow = Math.floor( $list.width() / $items.width() );
            if( perRow == null || perRow < 2 ) return true;

            for( var i = 0, j = $items.length; i < j; i += perRow )
            {
                var maxHeight   = 0,
                    $row        = $items.slice( i, i + perRow );

                $row.each( function()
                {
                    var itemHeight = parseInt( $( this ).outerHeight() );
                    if ( itemHeight > maxHeight ) maxHeight = itemHeight;
                });
                $row.css( 'height', maxHeight );
            }
        };

    setHeights();
    $( window ).on( 'resize', setHeights );



    var loadImages = function()
    {
        $items.filter( '.js-load-images:first' ).each( function()
        {
            var $this       = $( this ),
                $imgs       = $this.find( 'noscript.list__item__image' ),
                imgTotal    = $imgs.length,
                imgLoaded   = 0;

            $imgs.each( function()
            {
                var $noscript   = $( this ),
                    $img        = $( $noscript.text() );

                $img.load( function()
                {
                    $noscript.replaceWith( $img );
                    imgLoaded++;
                    if( imgLoaded >= imgTotal )
                    {
                        $this.css( 'opacity', 1 );
                        setHeights();
                        loadImages();
                    }
                });
            });
        });
    };

    $items.addClass( 'js-load-images' );
    loadImages();

})( jQuery, window, document );



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

    //$('.modal__new-countdown').on('click', function(e){
    //    e.preventDefault();
    //    if( e.target !== this )
    //        return;
    //    $('.modal__new-countdown').removeClass('show');
    //});

    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1;
    var yyyy = today.getFullYear();

    $('#id_end_date').pickmeup({
        flat    : false,
        min     : yyyy+'-'+mm+'-'+dd,
        format  : 'Y-m-d'
    });

    $('.submit input').on('click', function(e) {
        e.preventDefault();
        console.log('KAI :: submit click handler');
        app.createNewCountdown();
    });
};


app.createNewCountdown = function() {
    console.log('KAI :: creating new countdown');

    //var title = "test";
    //var description = "test description";
    //var end_datetime = new Date().toISOString();
    ////var image = $('.new-countdown-image').val();
    app.setupcsrf();

    //$.ajax({
    //    type: "POST",
    //    data: new FormData(form),
    //    //data: form(data),
    //    url: "/api/countdowns/create" ,
    //    success: function(data) {
    //
    //    },
    //    error: function(){
    //        console.log('KAI :: an error occured');
    //    }
    //});

    var form = $('#new-countdown-form');
    //form.submit(function () {
        $.ajax({
            type: form.attr('method'),
            url: "/api/countdowns/create" ,
            data: new FormData(form),
            success: function (data) {
                if (data) {
                    console.log('KAI :: data', data);
                    if(data.status == 200) {
                        app.createCountdownHTML(data);
                    }
                }
            },
            error: function(data) {
                console.log('KAI :: an error occured');
            }
        });
        return false;
    //});




};



app.createCountdownHTML = function(data) {
    console.log('KAI:: response', data.response);
    console.log('KAI:: status', data.status);

    var cd_div = document.createElement('div');
    cd_div.className = 'countdown';


    var cd_image = document.createElement('img');
    cd_image.className = 'countdown__image';
    cd_image.src = "/static/countdown/img/image-1.png";
    cd_div.appendChild(cd_image);

    var cd_content = document.createElement('div');
    cd_content.className = 'countdown__content';
    cd_div.appendChild(cd_content);


    var cd_time = document.createElement('p');
    cd_time.className = 'countdown__time';
    cd_time.innerHTML = '<span class="days">2</span> days <span class="hours">13</span> hours <span class="minutes">45</span> minutes';
    cd_content.appendChild(cd_time);


    var cd_title = document.createElement('p');
    cd_title.className = 'countdown__title capitalize';
    cd_title.innerHTML = "Dave's a dick";
    cd_content.appendChild(cd_title);

    var cd_desc = document.createElement('p');
    cd_desc.className = 'countdown__desc';
    cd_desc.innerHTML = "Dipiscing lorem fells a ante. Proin consequat a justo sed ornare Vestibulum quis magna vel nunc vehicula mattis ld eget lorem";
    cd_content.appendChild(cd_desc);

    $('.grid').get(0).insertBefore(cd_div, $('.countdown__empty').get(0));
    $('.modal__new-countdown').removeClass('show');
};


app.setupcsrf = function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
};



$( document ).ready(function() {
    app.initialize();
});


