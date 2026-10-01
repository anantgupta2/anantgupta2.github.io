/* Anant Gupta — site interactions: theme toggle, pub filters, scroll-spy nav */
(function () {
  "use strict";

  /* ---------- Theme toggle ---------- */
  var root = document.documentElement;
  var toggle = document.getElementById("theme-toggle");

  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("theme", next);
    });
  }

  // Follow the OS setting until the user picks a theme explicitly.
  var mq = window.matchMedia("(prefers-color-scheme: dark)");
  mq.addEventListener("change", function (e) {
    if (!localStorage.getItem("theme")) {
      root.setAttribute("data-theme", e.matches ? "dark" : "light");
    }
  });

  /* ---------- Publication filters ---------- */
  var chips = document.querySelectorAll(".chip[data-filter]");
  var pubs = document.querySelectorAll(".pub");

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var want = chip.dataset.filter;

      chips.forEach(function (c) {
        c.classList.toggle("is-active", c === chip);
      });

      pubs.forEach(function (pub) {
        pub.hidden = want !== "all" && pub.dataset.cat !== want;
      });
    });
  });

  /* ---------- Nav: border once scrolled, highlight current section ---------- */
  var nav = document.getElementById("nav");
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav__links a[href^='#']"));
  var sections = links
    .map(function (a) {
      return document.querySelector(a.getAttribute("href"));
    })
    .filter(Boolean);

  function onScroll() {
    if (nav) nav.classList.toggle("is-stuck", window.scrollY > 8);

    // The section whose top is closest to (but above) the scroll line wins.
    var line = window.scrollY + 120;
    var currentId = null;

    sections.forEach(function (sec) {
      if (sec.offsetTop <= line) currentId = sec.id;
    });

    links.forEach(function (a) {
      a.classList.toggle("is-current", a.getAttribute("href") === "#" + currentId);
    });
  }

  var ticking = false;
  window.addEventListener(
    "scroll",
    function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        onScroll();
        ticking = false;
      });
    },
    { passive: true }
  );

  onScroll();
})();
