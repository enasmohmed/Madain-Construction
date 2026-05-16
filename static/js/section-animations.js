/**
 * Scroll reveal for home page sections + staggered children.
 * Respects prefers-reduced-motion.
 */
(function () {
  "use strict";

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  var page = document.querySelector(".page-content");
  if (!page) {
    return;
  }

  function markItem(el, index, step) {
    el.classList.add("section-reveal__item");
    el.style.transitionDelay = index * (step || 0.1) + "s";
  }

  function setupSection(section) {
    if (!section || section.classList.contains("section-reveal")) {
      return;
    }
    section.classList.add("section-reveal");

    if (section.classList.contains("home-services")) {
      section.classList.add("home-services--interactive");
      var header = section.querySelector(".home-services__header");
      if (header) {
        markItem(header, 0, 0.08);
      }
      var note = section.querySelector(".home-services__intro-note");
      if (note) {
        markItem(note, 1, 0.08);
      }
      section.querySelectorAll(".home-services__col").forEach(function (col, i) {
        markItem(col, i + 2, 0.12);
      });
      return;
    }

    if (
      section.classList.contains("simply-home-offer") ||
      section.classList.contains("htc__offer__area")
    ) {
      section.querySelectorAll(".simply-home-offer__card, .offer").forEach(function (el, i) {
        markItem(el, i, 0.12);
      });
      return;
    }

    if (section.classList.contains("our-work-marquee-section")) {
      var title = section.querySelector(".section__title");
      if (title) {
        markItem(title, 0, 0.08);
      }
      var marquee = section.querySelector(".our-work-marquee");
      if (marquee) {
        markItem(marquee, 1, 0.12);
      }
      return;
    }

    if (section.classList.contains("mvv-split")) {
      var media = section.querySelector(".mvv-split__media");
      var panel = section.querySelector(".mvv-split__panel");
      if (media) {
        markItem(media, 0, 0.15);
      }
      if (panel) {
        markItem(panel, 1, 0.15);
      }
      return;
    }

    if (section.classList.contains("final-word")) {
      var fwTitle = section.querySelector(".final-word__header");
      if (fwTitle) {
        markItem(fwTitle, 0, 0.08);
      }
      section.querySelectorAll(".final-word__card, .final-word__col").forEach(function (el, i) {
        markItem(el, i + 1, 0.1);
      });
      return;
    }

    if (section.classList.contains("simply-contact")) {
      var inner = section.querySelector(".simply-contact__inner");
      if (inner) {
        markItem(inner, 0, 0.1);
      }
    }
  }

  page.querySelectorAll("section").forEach(setupSection);

  var hero = document.querySelector(".slider__container, .hero-video-root");
  if (hero) {
    hero.classList.add("section-reveal", "section-reveal--hero");
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) {
          return;
        }
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -5% 0px" }
  );

  document.querySelectorAll(".section-reveal").forEach(function (el) {
    observer.observe(el);
  });
})();
