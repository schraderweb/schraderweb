
    $(document).ready(function () {
      $('#nav0').click(function () {
        document.getElementById("submenu2").style.display = "none";
        document.getElementById("submenu").style.display = "block";
      });

      $('#nav1').click(function () {

        document.getElementById("submenu2").style.display = "block";

        document.getElementById("submenu").style.display = "none";
      });


     document.querySelectorAll("#nav a").forEach((el) => {
        if(el.hasAttribute("title") ){

        }else{
          el.remove();
        }
     })




      $('#body').click(function () {
        document.getElementById("submenu2").style.display = "none";
        document.getElementById("submenu").style.display = "none";
      });


      $('#nav0submenu').click(function () {

        if ($("#ulsubmenu1").hasClass("show-touch-menu") == false) {

          $("#ulsubmenu1").addClass("show-touch-menu");
        } else {
          $("#ulsubmenu1").removeClass("show-touch-menu");
        }
      });

      $('#nav1submenu').click(function () {

        if ($("#ulsubmenu2").hasClass("show-touch-menu") == false) {

          $("#ulsubmenu2").addClass("show-touch-menu");
        } else {
          $("#ulsubmenu2").removeClass("show-touch-menu");
        }
      });


      // menu click event
      $('#actionMenubutton').click(function () {

        $("#actionMenu").css("left", 0);
        $("#actionMenu").css("opacity", 1);
        $("#actionMenu").css("transform", "scale(1)");
        $("#actionNavMobileContainer").css("left", 0);
        $("#actionNavMobileContainer").css("opacity", 1);
        $("#actionNavMobileContainer").css("transform", "scale(1)");

      });
    });

    $('#closebutton').click(function () {
      $("#actionMenu").css("left", "-200vw");
      $("#actionMenu").css("opacity", 0);
      $("#actionMenu").css("transform", "scale(1)");
      $("#actionNavMobileContainer").css("left", "-200vw");
      $("#actionNavMobileContainer").css("opacity", 0);
      $("#actionNavMobileContainer").css("transform", "scale(1.5)");

      if ($("#ulsubmenu2").hasClass("show-touch-menu")) {

        $("#ulsubmenu2").removeClass("show-touch-menu");
      }

      if ($("#ulsubmenu1").hasClass("show-touch-menu")) {
        $("#ulsubmenu1").removeClass("show-touch-menu");
      }


    });


    function isOnScreen(elem) {
      // if the element doesn't exist, abort
      if (elem.length == 0) {
        return;
      }
      var $window = jQuery(window)
      var viewport_top = $window.scrollTop()
      var viewport_height = $window.height()
      var viewport_bottom = viewport_top + viewport_height
      var $elem = jQuery(elem)
      var top = $elem.offset().top
      var height = $elem.height()
      var bottom = top + height

      return (top >= viewport_top && top < viewport_bottom) ||
        (bottom > viewport_top && bottom <= viewport_bottom) ||
        (height > viewport_height && top <= viewport_top && bottom >= viewport_bottom)
    }


    $(function () {
      $('.rect').on('wheel', function (event) {
        if (event.originalEvent.deltaY < 0) {


          if (isOnScreen(jQuery('#sectionHomeWeb'))) {
            var offset = $('#sectionHomeBanner').offset();
            offset.left -= 0;
            offset.top -= 0;
            $('html, body').animate({
              scrollTop: offset.top,
              scrollLeft: offset.left
            });
            return false;
          }

          if (isOnScreen(jQuery('#sectionHomeSeo'))) {

            var offset = $('#sectionHomeWeb').offset();
            offset.left -= 0;
            offset.top -= 0;
            $('html, body').animate({
              scrollTop: offset.top,
              scrollLeft: offset.left
            });
            return false;
          }


          if (isOnScreen(jQuery('#sectionHomeSocial'))) {
            var offset = $('#sectionHomeSeo').offset();
            offset.left -= 0;
            offset.top -= 0;
            $('html, body').animate({
              scrollTop: offset.top,
              scrollLeft: offset.left
            });
            return false;
          }

          if (isOnScreen(jQuery('#sectionHomeContact'))) {
            var offset = $('#sectionHomeSocial').offset();
            offset.left -= 0;
            offset.top -= 0;
            $('html, body').animate({
              scrollTop: offset.top,
              scrollLeft: offset.left
            });
            return false;
          }

          if (isOnScreen(jQuery('#sectionFooter'))) {
            var offset = $('#sectionHomeContact').offset();
            offset.left -= 0;
            offset.top -= 0;
            $('html, body').animate({
              scrollTop: offset.top,
              scrollLeft: offset.left
            });
            return false;

          }



        } else {


          if (isOnScreen(jQuery('#sectionHomeBanner'))) {
            var offset = $('#sectionHomeWeb').offset();
            offset.left -= 0;
            offset.top -= 0;
            $('html, body').animate({
              scrollTop: offset.top,
              scrollLeft: offset.left
            });

            return false;
          }
          if (isOnScreen(jQuery('#sectionHomeWeb'))) {
            var offset = $('#sectionHomeSeo').offset();
            offset.left -= 0;
            offset.top -= 0;
            $('html, body').animate({
              scrollTop: offset.top,
              scrollLeft: offset.left
            });

            return false;

          }

          if (isOnScreen(jQuery('#sectionHomeSeo'))) {
            var offset = $('#sectionHomeSocial').offset();
            offset.left -= 0;
            offset.top -= 0;
            $('html, body').animate({
              scrollTop: offset.top,
              scrollLeft: offset.left
            });

            return false;
          }




          if (isOnScreen(jQuery('#sectionHomeSocial'))) {
            var offset = $('#sectionHomeContact').offset();
            offset.left += 35;
            offset.top += 35;
            $('html, body').animate({
              scrollTop: offset.top,
              scrollLeft: offset.left
            });

            return false;

          }



          if (isOnScreen(jQuery('#sectionHomeContact'))) {
            var offset = $('#social-media').offset();
            offset.left += 50;
            offset.top += 50;
            $('html, body').animate({
              scrollTop: offset.top,
              scrollLeft: offset.left
            });
            return false;
          }






        }
        return false;
      });
    });

