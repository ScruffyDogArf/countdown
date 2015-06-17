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


    //var loadImages = function()
    //{
    //    $items.filter( '.js-load-images:first' ).each( function()
    //    {
    //        var $this       = $( this ),
    //            $imgs       = $this.find( 'noscript.list__item__image' ),
    //            imgTotal    = $imgs.length,
    //            imgLoaded   = 0;
    //
    //        $imgs.each( function()
    //        {
    //            var $noscript   = $( this ),
    //                $img        = $( $noscript.text() );
    //
    //            $img.load( function()
    //            {
    //                $noscript.replaceWith( $img );
    //                imgLoaded++;
    //                if( imgLoaded >= imgTotal )
    //                {
    //                    $this.css( 'opacity', 1 );
    //                    setHeights();
    //                    loadImages();
    //                }
    //            });
    //        });
    //    });
    //};
    //
    //$items.addClass( 'js-load-images' );
    //loadImages();

})( jQuery, window, document );



var app = {};


app.initialize = function () {
    $('.username').on('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        console.log('KAI :: username click');
        $('.username-dropdown').toggleClass('show');
    });

    $('.countdown__menu-icon').on('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        console.log('KAI :: username click');
        $('.countdown__menu').not($(this).parent()).removeClass('show');
        $(this).parent().toggleClass('show');
    });

    $('html').click(function() {
        $('.username-dropdown').removeClass('show');
        $('.modal__bg-wrapper').removeClass('show');
        $('.countdown__menu').removeClass('show');
        //$('.content').foggy(false);

        //app.unlockScroll();
    });

    $('.username-dropdown').on('click', function(e){
        e.stopPropagation();
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


    $.mask.definitions['1']='[0-1]';
    $.mask.definitions['2']='[0-2]';
    $.mask.definitions['3']='[0-3]';
    $.mask.definitions['5']='[0-5]';
    $('#id_end_date').mask("9999-19-39").attr('placeholder','YYYY-MM-DD');
    $('#id_end_time').mask("29:59:59").attr('placeholder','HH:MM:SS');


    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1;
    var yyyy = today.getFullYear();

    $('#id_end_date').pickmeup({
        flat    : false,
        min     : yyyy+'-'+mm+'-'+dd,
        format  : 'Y-m-d',
        hide_on_select: true
    });


    $('#new-countdown-form').on('submit',(function(e) {
        e.preventDefault();
        var formData = new FormData(this);

        $.ajax({
            type:'POST',
            url: $(this).attr('action'),
            data:formData,
            cache:false,
            contentType: false,
            processData: false,
            success:function(data){
                console.log("success");
                console.log(data);
                app.createCountdownHTML(data);
            },
            error: function(data){
                console.log("error");
                console.log(data);
            }
        });
    }));
};



app.createCountdownHTML = function(data) {
    console.log('KAI:: response', data.response);
    console.log('KAI:: status', data.status);

    var cd_div = document.createElement('div');
    cd_div.className = 'countdown';

    var cd_menu = document.createElement('div');
    cd_menu.className = 'countdown__menu';
    cd_menu.innerHTML = '<div class="countdown__menu-icon"></div>' +
                        '<div class="countdown__menu-dropdown">' +
                        '<a href="#" class="edit-button blue-button button">edit</a>' +
                        '<a href="#" class="delete-button red-button button">delete</a>'+
                        '</div>';
    cd_div.appendChild(cd_menu);

    var cd_image = document.createElement('img');
    cd_image.className = 'countdown__image';
    cd_image.src = data.image;
    cd_div.appendChild(cd_image);

    var cd_content = document.createElement('div');
    cd_content.className = 'countdown__content';
    cd_div.appendChild(cd_content);


    var cd_time = document.createElement('p');

    var timeRemainingHTML = '';

    if (data.days > 0) {
        timeRemainingHTML += '<span class="days">'+ data.days +'</span> day';
        if (data.days > 1) {
            timeRemainingHTML += 's';
        }
        timeRemainingHTML += ' ';
    }

    if (data.hours > 0) {
        timeRemainingHTML += '<span class="hours">'+ data.hours +'</span> hour';
        if (data.hours > 1) {
            timeRemainingHTML += 's';
        }
        timeRemainingHTML += ' ';
    }

    if (data.minutes > 0) {
        timeRemainingHTML += '<span class="minutes">'+ data.minutes +'</span> minute';
        if (data.minutes > 1) {
            timeRemainingHTML += 's';
        }
        timeRemainingHTML += ' ';
    }

    if (data.seconds > 0) {
        timeRemainingHTML += '<span class="seconds">'+ data.seconds +'</span> second';
        if (data.seconds > 1) {
            timeRemainingHTML += 's';
        }
    }

    if (timeRemainingHTML == '') {
        timeRemainingHTML = 'COMPLETE';
        cd_time.className = 'countdown__complete';
    } else {
        cd_time.className = 'countdown__time';
    }


    cd_time.innerHTML = timeRemainingHTML;
    cd_content.appendChild(cd_time);


    var cd_title = document.createElement('p');
    cd_title.className = 'countdown__title capitalize';
    cd_title.innerHTML = data.title;
    cd_content.appendChild(cd_title);

    var cd_desc = document.createElement('p');
    cd_desc.className = 'countdown__desc';
    cd_desc.innerHTML = data.brief_description;
    cd_content.appendChild(cd_desc);

    $('.grid').get(0).insertBefore(cd_div, $('.countdown__empty').get(0));
    $('.modal__new-countdown').removeClass('show');

    setTimeout(function(){app.setHeights()}, 1000);
};


app.setHeights = function() {

    console.log('KAI :: setting heights');
    var $list       = $( '.grid' ),
        $items      = $list.find( '.countdown' );

        $items.css( 'height', 'auto' );

        var perRow = Math.floor( $list.width() / $items.width() );
        //if( perRow == null || perRow < 2 ) return true;

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


