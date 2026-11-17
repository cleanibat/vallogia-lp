/* Le tracking est géré par GTM (déclencheurs natifs « Envoi de formulaire » et clic tel:). */
(function () {
  "use strict";
  /* Formulaire multi-étapes façon Typeform : une question à la fois, envoi classique en POST à la fin. */
  document.querySelectorAll("form.tf").forEach(function (f) {
    var steps = [].slice.call(f.querySelectorAll(".tf-step")), i = 0;
    var bar = f.querySelector(".tf-progress span"), count = f.querySelector(".tf-count b"), back = f.querySelector(".tf-back");
    f.classList.add("tf-on");
    function show(n, focus) {
      i = n;
      steps.forEach(function (s, k) { s.classList.toggle("is-active", k === n); });
      bar.style.width = ((n + 1) / steps.length * 100) + "%";
      count.textContent = n + 1; back.hidden = n === 0;
      if (focus && f.getBoundingClientRect().top < 70) f.scrollIntoView({ behavior: "smooth" }); /* mobile : garder la question en vue */
      if (focus) { var el = steps[n].querySelector("input:not([type=radio]),textarea"); if (el) el.focus({ preventScroll: true }); }
    }
    function valid(s) {
      var els = s.querySelectorAll("input,textarea");
      for (var k = 0; k < els.length; k++) { if (!els[k].checkValidity()) { els[k].reportValidity(); return false; } }
      return true;
    }
    function next() { if (valid(steps[i]) && i < steps.length - 1) show(i + 1, true); }
    f.querySelectorAll(".tf-choice input").forEach(function (r) {
      r.addEventListener("change", function () { setTimeout(next, 220); });
    });
    f.querySelectorAll(".tf-next").forEach(function (b) { b.addEventListener("click", next); });
    back.addEventListener("click", function () { if (i > 0) show(i - 1, false); });
    f.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && e.target.tagName === "INPUT" && i < steps.length - 1) { e.preventDefault(); next(); }
    });
    /* Raccourcis clavier A, B, C… sur les étapes à choix (comme Typeform) */
    document.addEventListener("keydown", function (e) {
      if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) && e.target.type !== "radio") return;
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      var r = f.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return; /* formulaire visible uniquement */
      var opts = steps[i].querySelectorAll(".tf-choice input"), k = e.key.toUpperCase().charCodeAt(0) - 65;
      if (e.key.length === 1 && opts[k]) { opts[k].checked = true; opts[k].dispatchEvent(new Event("change")); }
    });
    /* Si un champ d'une étape cachée est invalide à l'envoi, on y revient */
    f.addEventListener("invalid", function (e) {
      var k = steps.indexOf(e.target.closest(".tf-step")); if (k > -1 && k !== i) show(k, true);
    }, true);
    show(0, false);
  });
  /* Bouton d'envoi : état « Envoi… » après validation HTML5 (aucun effet sur GTM) */
  document.querySelectorAll("form").forEach(function (f) {
    f.addEventListener("submit", function () {
      if (!f.checkValidity()) return;
      var b = f.querySelector("button[type=submit]"); if (b) { b.disabled = true; b.textContent = b.getAttribute("data-sending") || "Envoi…"; }
    });
  });
})();
