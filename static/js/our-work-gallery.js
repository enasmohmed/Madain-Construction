/**
 * Our work marquee — clone columns, autoplay thumbnails, lightbox on click.
 */
(function () {
  "use strict";

  function resolveMediaSrc(raw) {
    if (!raw) {
      return "";
    }
    try {
      return new URL(raw, window.location.href).href;
    } catch (err) {
      return raw;
    }
  }

  function initOurWorkSection(section) {
    var root = section.querySelector("[data-our-work-marquee]");
    var modal = section.querySelector(".our-work-lightbox");
    if (!root || !modal) {
      return;
    }

    root.querySelectorAll(".our-work-marquee__col").forEach(function (column) {
      if (column.dataset.marqueeCloned === "1") {
        return;
      }
      var wraps = Array.prototype.slice.call(
        column.querySelectorAll(".our-work-marquee__wrap")
      );
      if (!wraps.length) {
        return;
      }
      wraps.forEach(function (wrap) {
        column.appendChild(wrap.cloneNode(true));
      });
      column.dataset.marqueeCloned = "1";
    });

    function startMarqueeVideos(container) {
      container.querySelectorAll(".our-work-marquee__video").forEach(function (v) {
        v.muted = true;
        v.defaultMuted = true;
        v.loop = true;
        v.playsInline = true;
        v.setAttribute("playsinline", "");
        v.setAttribute("muted", "");
        v.setAttribute("loop", "");
        v.autoplay = true;

        function tryPlay() {
          v.play().catch(function () {});
        }

        if (v.readyState >= 2) {
          tryPlay();
        } else {
          v.addEventListener("loadeddata", tryPlay, { once: true });
          v.addEventListener("canplay", tryPlay, { once: true });
        }
      });
    }

    startMarqueeVideos(root);

    var bodyEl = modal.querySelector(".our-work-lightbox__body");
    var closeEls = modal.querySelectorAll("[data-our-work-lightbox-close]");

    function closeModal() {
      bodyEl.querySelectorAll("video").forEach(function (v) {
        v.pause();
      });
      bodyEl.innerHTML = "";
      modal.hidden = true;
      modal.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      document.removeEventListener("keydown", onKeydown);
    }

    function onKeydown(e) {
      if (e.key === "Escape") {
        closeModal();
      }
    }

    function openModal(src, isVideo) {
      var mediaSrc = resolveMediaSrc(src);
      if (!mediaSrc) {
        return;
      }

      bodyEl.innerHTML = "";

      if (isVideo) {
        var v = document.createElement("video");
        v.className = "our-work-lightbox__media";
        v.src = mediaSrc;
        v.controls = true;
        v.playsInline = true;
        v.preload = "auto";
        v.setAttribute("playsinline", "");
        v.setAttribute("controls", "");
        bodyEl.appendChild(v);
        v.play().catch(function () {});
      } else {
        var im = document.createElement("img");
        im.src = mediaSrc;
        im.alt = "";
        im.className = "our-work-lightbox__media";
        bodyEl.appendChild(im);
      }

      modal.hidden = false;
      modal.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      document.addEventListener("keydown", onKeydown);
      modal.querySelector(".our-work-lightbox__close").focus();
    }

    root.addEventListener("click", function (e) {
      var wrap = e.target.closest(".our-work-marquee__wrap");
      if (!wrap || !root.contains(wrap)) {
        return;
      }

      e.preventDefault();

      var mediaSrc = wrap.getAttribute("data-media-src");
      var mediaType = wrap.getAttribute("data-media-type");

      if (!mediaSrc) {
        var img = wrap.querySelector("img");
        var vid = wrap.querySelector("video");
        if (img) {
          mediaSrc = img.currentSrc || img.getAttribute("src");
          mediaType = "image";
        } else if (vid) {
          mediaSrc = vid.currentSrc || vid.getAttribute("src");
          mediaType = "video";
        }
      }

      openModal(mediaSrc, mediaType === "video");
    });

    root.addEventListener("keydown", function (e) {
      if (e.key !== "Enter" && e.key !== " ") {
        return;
      }
      var wrap = e.target.closest(".our-work-marquee__wrap");
      if (!wrap || !root.contains(wrap)) {
        return;
      }
      e.preventDefault();
      wrap.click();
    });

    closeEls.forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        closeModal();
      });
    });
  }

  function boot() {
    document.querySelectorAll(".our-work-marquee-section").forEach(initOurWorkSection);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
