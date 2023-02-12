$(document).ready(function () {
  window.addEventListener("load", function () {
    // Initialize AOS
    AOS.init();
  });

  const openIcon = document.getElementById("openOrClose");
  const navMenu = document.getElementById("the-nav-menu");

  const allNavbarLinks = document.querySelectorAll("nav a");
  let navbarLinksTotalCount = allNavbarLinks.length;

  openIcon.addEventListener("click", function () {
    currentIcon = this.className;
    if (currentIcon == "fa fa-bars") {
      this.classList = "fa fa-times";
      navMenu.classList.add("active");
      document.body.style["overflow-y"] = "hidden";
    } else {
      this.classList = "fa fa-bars";
      navMenu.classList.remove("active");
      document.body.style["overflow-y"] = "auto";
    }
  });

  for (let i = 0; i < navbarLinksTotalCount; i++) {
    allNavbarLinks[i].classList.remove("active");
    const link = allNavbarLinks[i];
    link.addEventListener("click", function () {
      openIcon.className = "fa fa-bars";
      navMenu.classList.remove("active");
      document.body.style["overflow-y"] = "auto";
    });
  }

  $(document).click(function (e) {
    if (!$(e.target).closest("#crazy").length) {
      $("#crazy").prop("checked", false);
    }
  });

  $("a.active").removeClass("active");
  $('a[href="' + location.pathname + '"]')
    .closest("a")
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
    $("#message_div").fadeToggle();
  });

  $("#unread_but").addClass("active");
  $("#unread_filter_section").show();
  $("#all_filter_section").hide();
  $("#read_filter_section").hide();

  $(".carousel-item").eq(0).addClass("active");
});
