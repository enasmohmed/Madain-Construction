/*-----------------------------------------------------------------------------------

  Template Name: Simply Construction HTML Template.
  Template URI: #
  Description: Simply Construction is a unique website template designed in HTML with a simple & beautiful look. There is an excellent solution for creating clean, wonderful and trending material design corporate, corporate any other purposes websites.
  Author: DevItems
  Version: 1.0

-----------------------------------------------------------------------------------*/

/*-------------------------------
[  Table of contents  ]
---------------------------------
  01. jQuery MeanMenu
  02. wow js active
  03. Project  Masonry
  04. Sticky Header
  05. ScrollUp
  06. Testimonial Slick Carousel
  07. Testimonial Slick Carousel
  08. CounterUp
  16. ScrollReveal Js Init
  17. Magnific Popup




/*--------------------------------
[ End table content ]
-----------------------------------*/


(function($) {
    'use strict';


/*-------------------------------------------
  01. jQuery MeanMenu
--------------------------------------------- */
    
$('.mobile-menu nav').meanmenu({
    meanMenuContainer: '.mobile-menu-area',
    meanScreenWidth: '991',
    meanRevealPosition: 'right',
});
/*-------------------------------------------
  02. wow js active
--------------------------------------------- */
    new WOW().init();


/*-------------------------------------------
  03. Project  Masonry
--------------------------------------------- */ 

if ($('.htc__project__container').length && $('.htc__latest__project__wrap').length) {
  $('.htc__project__container').imagesLoaded(function () {
    var $grid = $('.htc__latest__project__wrap').isotope({
      itemSelector: '.single__project',
      percentPosition: true,
      transitionDuration: '0.7s',
      layoutMode: 'fitRows',
      masonry: {
        columnWidth: '.single__project',
      },
    });
    $('.project__menu').on('click', 'button', function () {
      var filterValue = $(this).attr('data-filter');
      $grid.isotope({ filter: filterValue });
    });
  });
}

$('.project__menu button').on('click', function(event) {
    $(this).siblings('.is-checked').removeClass('is-checked');
    $(this).addClass('is-checked');
    event.preventDefault();
});



/*-------------------------------------------
  04. Sticky Header
--------------------------------------------- */ 

  $(window).on('scroll',function() {    
    var scroll = $(window).scrollTop();
    if (scroll < 245) {
    $("#sticky-header-with-topbar").removeClass("scroll-header");
    }else{
    $("#sticky-header-with-topbar").addClass("scroll-header");
    }
  });


/*--------------------------
  05. ScrollUp
---------------------------- */

  $.scrollUp({
    /* Font Awesome 4 (المحمّل في القالب) — zmdi غير مضمّن فكان الزر يبدو فارغًا */
    scrollText: '<i class="fa fa-chevron-up" aria-hidden="true"></i>',
    scrollTitle: 'Back to top',
    scrollDistance: 200,
    zIndex: 10060,
    easingType: 'linear',
    scrollSpeed: 900,
    animation: 'fade',
    animationSpeed: 450
  });

  (function initScrollUpEnterFx() {
    var $btn = $('#scrollUp');
    if (!$btn.length) {
      return;
    }

    var wasVisible = false;
    var threshold = 200;

    $(window).on('scroll.scrollUpFx', function () {
      var isVisible = $(window).scrollTop() > threshold;

      if (isVisible && !wasVisible) {
        $btn.removeClass('scroll-up--enter');
        if ($btn[0]) {
          void $btn[0].offsetWidth;
        }
        $btn.addClass('scroll-up--enter');
      }

      if (!isVisible) {
        $btn.removeClass('scroll-up--enter');
      }

      wasVisible = isVisible;
    });

    $btn.on('animationend webkitAnimationEnd', function (e) {
      var name = e.originalEvent && e.originalEvent.animationName;
      if (name === 'scroll-up-pop') {
        $btn.removeClass('scroll-up--enter');
      }
    });
  })();


/*---------------------------------------------
  06. Testimonial Slick Carousel
------------------------------------------------*/
  if ($('.testimonial__activation').length) {
    $('.testimonial__activation').slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      arrows: false,
      draggable: true,
      // fade: true,
      dots: true,
    });
  }


/*------------------------------------------
  07. Testimonial Slick Carousel
-------------------------------------------*/
  if ($('.testimonial__activation--2').length) {
    $('.testimonial__activation--2').slick({
      slidesToShow: 2,
      slidesToScroll: 2,
      arrows: false,
      draggable: true,
      // fade: true,
      dots: true,
    });
  }



/*-----------------------------
  08. CounterUp
-----------------------------*/
  $('.count').counterUp({
    delay: 60,
    time: 3000
  });






/*-----------------------------------------------
  15. Home Slider (هيرو الصفحة الرئيسية + أي سلايدر قديم بنفس الكلاس)
-------------------------------------------------*/

  function initHeroHomeCarousel() {
    var $hero = $('#heroHomeCarousel');
    if (!$hero.length || $hero.hasClass('owl-loaded')) {
      return;
    }
    var slideCount = $hero.children('.slide').length;
    if (slideCount < 1) {
      return;
    }
    var multi = slideCount > 1;
    /* Owl 2: loop مع شريحتين فقط غالبًا يعطل التنقل — نستخدم rewind بدل loop عند ≤2 */
    var useLoop = multi && slideCount > 2;
    $hero.owlCarousel({
      rtl: false,
      items: 1,
      margin: 0,
      loop: useLoop,
      rewind: multi && !useLoop,
      /* أسهم فقط عند وجود أكثر من شريحة؛ النقاط تظهر دائمًا كمرجع بصري */
      nav: multi,
      dots: true,
      autoplay: Boolean(multi),
      autoplayTimeout: 5500,
      autoplayHoverPause: true,
      smartSpeed: 650,
      navSpeed: 450,
      navText: [
        '<span class="hero-owl-nav-inner"><i class="fa fa-chevron-left" aria-hidden="true"></i></span>',
        '<span class="hero-owl-nav-inner"><i class="fa fa-chevron-right" aria-hidden="true"></i></span>'
      ],
      lazyLoad: false,
      mouseDrag: multi,
      touchDrag: multi,
      pullDrag: multi,
      responsive: {
        0: { items: 1 },
        600: { items: 1 }
      }
    });
    if (multi) {
      $hero.trigger('play.owl.autoplay');
    }
  }

  function initOtherHomeSliders() {
    $('.slider__activation__wrap').not('#heroHomeCarousel').each(function () {
      var $wrap = $(this);
      if ($wrap.hasClass('owl-loaded')) {
        return;
      }
      var slideCount = $wrap.children('.slide').length;
      if (!slideCount) {
        return;
      }
      var multi = slideCount > 1;
      var useLoop = multi && slideCount > 2;
      $wrap.owlCarousel({
        rtl: false,
        items: 1,
        margin: 0,
        loop: useLoop,
        rewind: multi && !useLoop,
        nav: multi,
        dots: multi,
        autoplay: Boolean(multi),
        autoplayTimeout: 5500,
        autoplayHoverPause: true,
        smartSpeed: 650,
        navSpeed: 450,
        navText: [
          '<span class="hero-owl-nav-inner"><i class="fa fa-chevron-left" aria-hidden="true"></i></span>',
          '<span class="hero-owl-nav-inner"><i class="fa fa-chevron-right" aria-hidden="true"></i></span>'
        ],
        lazyLoad: false,
        mouseDrag: multi,
        touchDrag: multi,
        pullDrag: multi,
        responsive: {
          0: { items: 1 },
          600: { items: 1 }
        }
      });
      if (multi) {
        $wrap.trigger('play.owl.autoplay');
      }
    });
  }

  $(function () {
    initHeroHomeCarousel();
    initOtherHomeSliders();
  });

  $(window).on('load', function () {
    var $hero = $('#heroHomeCarousel');
    if ($hero.length && $hero.hasClass('owl-loaded')) {
      $hero.trigger('refresh.owl.carousel');
      window.setTimeout(function () {
        if ($hero.find('.owl-item').length > 1) {
          $hero.trigger('play.owl.autoplay');
        }
      }, 150);
    }
  });



/*-----------------------------------
  16. ScrollReveal Js Init
-------------------------------------- */

  window.sr = ScrollReveal({ duration: 800 , reset: false });
    sr.reveal('.foo');
    sr.reveal('.bar');






/*--------------------------------
  17. Magnific Popup
----------------------------------*/

$('.video-popup').magnificPopup({
  type: 'iframe',
  mainClass: 'mfp-fade',
  removalDelay: 160,
  preloader: false,
  zoom: {
      enabled: true,
  }
});

$('.image-popup').magnificPopup({
  type: 'image',
  mainClass: 'mfp-fade',
  removalDelay: 100,
  gallery:{
      enabled:true, 
  }
});






/*-----------------------------------------------
  16. Blog Slider
-------------------------------------------------*/

  if ($('.blog__activation').length) {
    $('.blog__activation').owlCarousel({
      loop: true,
      margin:0,
      nav:true,
      autoplay: false,
      navText: [ '<i class="zmdi zmdi-chevron-left"></i>', '<i class="zmdi zmdi-chevron-right"></i>' ],
      autoplayTimeout: 10000,
      items:1,
      dots: false,
      lazyLoad: true,
      responsive:{
        0:{
          items:1
        },
        600:{
          items:1
        }
      }
    });
  }








})(jQuery);




