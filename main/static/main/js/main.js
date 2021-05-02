

$(document).ready(function (){
    AOS.init();

    // click to scroll top
    $('.move-up span').click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 1000);
    });

    $('li.active').removeClass('active');
    $('a[href="' + location.pathname + '"]').closest('li').addClass('active');

    const buttons = document.querySelector('.settings'),
        buttonsList = buttons.querySelectorAll('button'),
        totalButtons = buttonsList.length
    
    for (let i=0; i<totalButtons; i++){
        const a = buttonsList[i]
        a.addEventListener('click', function(){
            for (let j=0; j<totalButtons; j++){
                buttonsList[j].classList.remove('active');
            }
            this.classList.add('active');
        })
    };

    $('#profile-edit').show();
    $('#home-feed').hide();

    $('#profile').click(function () {
        $('#home-feed').hide();
        $('#profile-edit').show();
    });
    
    $('#feed').click(function () {
        $('#profile-edit').hide();
        $('#home-feed').show();
    });
    
});

