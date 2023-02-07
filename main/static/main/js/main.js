$(document).ready(function () {
  window.addEventListener("load", function () {
    // Initialize AOS
    AOS.init();
  });

  $(document).click(function (e) {
    if (!$(e.target).closest("#navbarNav").length) {
      $("#navbarNav").removeClass("show");
    }
    if (!$(e.target).closest("#crazy").length) {
      $("#crazy").prop("checked", false);
    }
  });

  $("li.active").removeClass("active");
  $('a[href="' + location.pathname + '"]')
    .closest("li")
    .addClass("active");

  $("#followers").addClass("active");
  $("#flwr_div").show();
  $("#flwng_div").hide();

  $("#followers").click(function () {
    $("#followers").addClass("active");
    $("#followings").removeClass("active");
    $("#flwr_div").show();
    $("#flwng_div").hide();
  });
  $("#followings").click(function () {
    $("#followings").addClass("active");
    $("#followers").removeClass("active");
    $("#flwr_div").hide();
    $("#flwng_div").show();
  });

  $("#profile").addClass("active");
  $("#profile-edit").show();
  $("#home-feed").hide();

  $("#profile").click(function () {
    $("#profile").addClass("active");
    $("#feed").removeClass("active");
    $("#home-feed").hide();
    $("#profile-edit").show();
  });

  $("#feed").click(function () {
    $("#feed").addClass("active");
    $("#profile").removeClass("active");
    $("#profile-edit").hide();
    $("#home-feed").show();
  });

  $("#paint_comments").addClass("active");
  $("#comments").show();
  $("#add_comment").hide();
  $("#add_try").hide();
  $("#tries").hide();

  $("#tried").click(function () {
    $("#tried").addClass("active");
    $("#paint_comments").removeClass("active");
    $("#show_inp").removeClass("active");
    $("#tries").show();
    $("#comments").hide();
    $("#add_comment").hide();
    $("#add_try").hide();
  });

  $("#paint_comments").click(function () {
    $("#paint_comments").addClass("active");
    $("#tried").removeClass("active");
    $("#show_inp").removeClass("active");
    $("#comments").show();
    $("#tries").hide();
    $("#add_comment").hide();
    $("#add_try").hide();
  });

  $("#show_inp").click(function () {
    $("#show_inp").addClass("active");
    $("#tried").removeClass("active");
    $("#paint_comments").removeClass("active");
    $("#comments").hide();
    $("#tries").hide();
    $("#add_comment").show();
    $("#add_try").hide();
  });

  $(".add_pho").click(function () {
    $("#add_try").show();
    $("#show_inp").removeClass("active");
    $("#tried").removeClass("active");
    $("#paint_comments").removeClass("active");
    $("#comments").hide();
    $("#tries").hide();
    $("#add_comment").hide();
  });

  $("#message_div").hide();

  $("#send_button").click(function () {
    $("#message_div").toggle();
  });

  $("#unread_but").addClass("active");
  $("#unread_filter_section").show();
  $("#all_filter_section").hide();
  $("#read_filter_section").hide();

  $(".carousel-item").eq(0).addClass("active");
  // $('div.carousel-inner > div:first-child').addClass('active')
});

// const filter = document.querySelector(".all_filter_but"),
//   all_filter_buttons = filter.querySelectorAll("button"),
//   totalButtons = all_filter_buttons.length;

// for (let i = 0; i < totalButtons; i++) {
//   const a = all_filter_buttons[i];
//   a.addEventListener("click", function () {
//     for (let j = 0; j < totalButtons; j++) {
//       all_filter_buttons[j].classList.remove("active");
//     }
//     this.classList.add("active");
//     if (this.innerHTML == "Read") {
//       $("#read_filter_section").show();
//       $("#unread_filter_section").hide();
//       $("#all_filter_section").hide();
//     } else if (this.innerHTML == "Unread") {
//       $("#unread_filter_section").show();
//       $("#all_filter_section").hide();
//       $("#read_filter_section").hide();
//     } else {
//       $("#all_filter_section").show();
//       $("#unread_filter_section").hide();
//       $("#read_filter_section").hide();
//     }
//   });
// }
