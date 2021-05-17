

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
    $('#add_try').hide()
    
    $('#tried').click(function(){
        $('#tried').addClass('active')
        $('#paint_comments').removeClass('active')
        $('#show_inp').removeClass('active')
        $('#tries').show()
        $('#comments').hide()
        $('#add_comment').hide()
        $('#add_try').hide()
    });
    
    $('#paint_comments').click(function(){
        $('#paint_comments').addClass('active')
        $('#tried').removeClass('active')
        $('#show_inp').removeClass('active')
        $('#comments').show()
        $('#tries').hide()
        $('#add_comment').hide()
        $('#add_try').hide()
    });
    
    $('#show_inp').click(function(){
        $('#show_inp').addClass('active')
        $('#tried').removeClass('active')
        $('#paint_comments').removeClass('active')
        $('#comments').hide()
        $('#tries').hide()
        $('#add_comment').show()
        $('#add_try').hide()
    });

    $('.add_pho').click(function(){
        $('#add_try').show()
        $('#show_inp').removeClass('active')
        $('#tried').removeClass('active')
        $('#paint_comments').removeClass('active')
        $('#comments').hide()
        $('#tries').hide()
        $('#add_comment').hide()
    })

    $('#message_div').hide()

    $('#send_button').click(function(){
        $('#message_div').show()
    })

    $('#unread_but').addClass('active')
    $('#unread_filter_section').show()
    $('#all_filter_section').hide()
    $('#read_filter_section').hide()

});


const filter = document.querySelector('.all_filter_but'),
    all_filter_buttons = filter.querySelectorAll('button'),
    totalButtons = all_filter_buttons.length;

for(let i=0; i<totalButtons; i++){
    const a = all_filter_buttons[i];
    a.addEventListener('click', function(){
        for(let j=0; j<totalButtons; j++){
            all_filter_buttons[j].classList.remove('active');            
        }
        this.classList.add('active');
        if(this.innerHTML == 'Read'){
            $('#read_filter_section').show()
            $('#unread_filter_section').hide()
            $('#all_filter_section').hide()
        }else if(this.innerHTML == 'Unread'){
            $('#unread_filter_section').show()
            $('#all_filter_section').hide()
            $('#read_filter_section').hide()
        }else{
            $('#all_filter_section').show()
            $('#unread_filter_section').hide()
            $('#read_filter_section').hide()
        }
    })
}
