

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


    $('#followers').addClass('active');
    $('#flwng_div').hide()

    $('#followers').click(function(){
        $('#followers').addClass('active')
        $('#followings').removeClass('active')
        $('#flwr_div').show()
        $('#flwng_div').hide()
    })
    $('#followings').click(function(){
        $('#followings').addClass('active')
        $('#followers').removeClass('active')
        $('#flwng_div').show()
        $('#flwr_div').hide()
    });

    $('#message_div').hide()

    $('#send_button').click(function(){
        $('#message_div').show()
    })

});

// Some other JS

// document.getElementById('clickme').onclick=function(){
//     var el =  document.getElementById('another');
//     if(el.style.display == ''){
//         el.style.display = 'none';
//     }else{
//         el.style.display = '';
//     }
// };



/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
// function myFunction() {
//     document.getElementById("myDropdown").classList.toggle("show");
//   }
  
//   // Close the dropdown menu if the user clicks outside of it
//   window.onclick = function(event) {
//     if (!event.target.matches('.dropbtn')) {
//       var dropdowns = document.getElementsByClassName("dropdown-content");
//       var i;
//       for (i = 0; i < dropdowns.length; i++) {
//         var openDropdown = dropdowns[i];
//         if (openDropdown.classList.contains('show')) {
//           openDropdown.classList.remove('show');
//         }
//       }
//     }
//   }
