

$(document).ready(function (){
    // AOS.init();

    // // click to scroll top
    // $('.move-up span').click(function () {
    //     $('html, body').animate({
    //         scrollTop: 0
    //     }, 1000);
    // });

    $('li.active').removeClass('active');
    $('a[href="' + location.pathname + '"]').closest('li').addClass('active');


    $('#profile').addClass('active');
    $('#profile-edit').show();
    $('#home-feed').hide();

    $('#profile').click(function () {
        $('#profile').addClass('active');
        $('#feed').removeClass('active');
        $('#home-feed').hide();
        $('#profile-edit').show();
    });
    
    $('#feed').click(function () {
        $('#feed').addClass('active')
        $('#profile').removeClass('active')
        $('#profile-edit').hide();
        $('#home-feed').show();
    });

    
    $('#tried').addClass('active')
    $('#tries').show()
    $('#comments').hide()
    $('#add_comment').hide()
    
    $('#tried').click(function(){
        $('#tried').addClass('active')
        $('#paint_comments').removeClass('active')
        $('#show_inp').removeClass('active')
        $('#tries').show()
        $('#comments').hide()
        $('#add_comment').hide()
    });
    
    $('#paint_comments').click(function(){
        $('#paint_comments').addClass('active')
        $('#tried').removeClass('active')
        $('#show_inp').removeClass('active')
        $('#comments').show()
        $('#tries').hide()
        $('#add_comment').hide()
    });
    
    $('#show_inp').click(function(){
        $('#show_inp').addClass('active')
        $('#tried').removeClass('active')
        $('#paint_comments').removeClass('active')
        $('#comments').hide()
        $('#tries').hide()
        $('#add_comment').show()
    });

});

